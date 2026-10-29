#!/usr/bin/env python3
import re
import itertools

TABLE_NAMES = ("cell_rise", "cell_fall", "rise_transition", "fall_transition")


def match_brace(text, i):
    assert text[i] == "{"
    depth = 0
    for k in range(i, len(text)):
        c = text[k]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return k
    raise ValueError("unbalanced braces")


def blocks(text, header_regex):
    out = []
    for m in re.finditer(header_regex, text):
        b = text.index("{", m.start())
        e = match_brace(text, b)
        out.append((m.start(), e + 1, m))
    return out


def cell_blocks(text):
    return {m.group(1): (s, e) for s, e, m in blocks(text, r"(?m)^\s*cell \((\w+)\) \{")}


def floats(s):
    return [float(x) for x in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", s)]


def get_index(block, n):
    m = re.search(r"index_%d \(\s*\\?\s*\"([^\"]*)\"" % n, block)
    return floats(m.group(1))


def get_values(block):
    m = re.search(r"values \(((?:\s*\\?\s*\"[^\"]*\"\s*,?)+)\s*\\?\s*\);", block)
    return [floats(r) for r in re.findall(r"\"([^\"]*)\"", m.group(1))]


def cell_info(cell_text):
    area = float(re.search(r"area : ([\d.eE+-]+);", cell_text).group(1))
    pins = {}
    for s, e, m in blocks(cell_text, r"(?m)^\s*pin \((\w+)\) \{"):
        pins[m.group(1)] = cell_text[s:e]
    inputs = [p for p, t in pins.items() if re.search(r"direction : input;", t)]
    outputs = [p for p, t in pins.items() if re.search(r"direction : output;", t)]
    info = dict(area=area, inputs=inputs, outputs=outputs, pins=pins, tables={}, function={})
    for o in outputs:
        fm = re.search(r"function : \"([^\"]*)\";", pins[o])
        info["function"][o] = fm.group(1) if fm else None
        for s, e, m in blocks(pins[o], r"(?m)^\s*timing \(\) \{"):
            t = pins[o][s:e]
            rel = re.search(r"related_pin : \"(\w+)\";", t).group(1)
            for name in TABLE_NAMES:
                for s2, e2, m2 in blocks(t, r"(?m)^\s*%s \(\w+\) \{" % name):
                    tb = t[s2:e2]
                    info["tables"].setdefault((rel, name), []).append(
                        (get_index(tb, 1), get_index(tb, 2), get_values(tb)))
    return info


def eval_function(expr, assign):
    if not re.fullmatch(r"[\w!&|+*() ]+", expr):
        raise ValueError("unsupported function syntax: %r" % expr)
    py = (expr.replace("!", " not ").replace("&", " and ").replace("*", " and ")
          .replace("|", " or ").replace("+", " or "))
    return bool(eval(py, {"__builtins__": {}}, {k: bool(v) for k, v in assign.items()}))


def sensitizing_states(expr, pin, inputs):
    others = [p for p in inputs if p != pin]
    res = []
    for bits in itertools.product((0, 1), repeat=len(others)):
        st = dict(zip(others, bits))
        if eval_function(expr, dict(st, **{pin: 0})) != eval_function(expr, dict(st, **{pin: 1})):
            res.append(st)
    return res


def when_expr(state):
    return "&".join(("" if v else "!") + k for k, v in state.items())

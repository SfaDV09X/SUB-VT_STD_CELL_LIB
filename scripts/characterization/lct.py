# Wrapper around lctime: python3 lct.py <points> <lctime args...>
# Patches the number of time points per transient in lctime's source (1e5 by default) before
# running it. With LCT_NOBREAK=1 it also skips lctime's extra simulator breakpoints
# (charflow.py uses this on retries).

import sys
N = float(sys.argv.pop(1))
import lctime.characterization.timing_combinatorial as tc
import lctime.characterization.input_capacitance as ic
import os
for mod, old, new in ((tc, "cfg.time_step * 1e5", "cfg.time_step * %g" % N), (ic, "cfg.time_step * 1e6", "cfg.time_step * %g" % (10 * N))):
    src = open(mod.__file__).read()
    if old not in src:
        sys.exit("lctime source layout not recognised: %s" % mod.__file__)
    src = src.replace(old, new)
    if mod is tc and os.environ.get("LCT_NOBREAK") == "1":
        if "simulation.set_breakpoint(" not in src:
            sys.exit("lctime source layout not recognised: %s" % mod.__file__)
        src = src.replace("simulation.set_breakpoint(", "(lambda *a_, **k_: None)(")
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
# Point lctime's main at the patched functions and run it.
import lctime.characterization.main_lctime as m
m.characterize_comb_cell = tc.characterize_comb_cell
m.characterize_input_capacitances = ic.characterize_input_capacitances
sys.exit(m.main())

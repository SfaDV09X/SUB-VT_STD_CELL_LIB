// Workload: Knuth-Morris-Pratt search for "baba" in a 240-character pseudo-random text
// (byte loads and branches); returns the match count mixed with the match positions.

#define TL 240
#define PL 4
static char text[TL];
static const char pat[PL] = {'b', 'a', 'b', 'a'};
static int fail[PL];

int main(void)
{
  unsigned int x = 0x13579bdfu;
  for (int i = 0; i < TL; i++) {
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    text[i] = (char)('a' + (x & 1u) + ((x >> 7) & (x >> 9) & 1u));
  }
  // Failure table of the pattern.
  int k = 0;
  fail[0] = 0;
  for (int q = 1; q < PL; q++) {
    while (k > 0 && pat[k] != pat[q])
      k = fail[k - 1];
    if (pat[k] == pat[q])
      k++;
    fail[q] = k;
  }
  // Scan the text.
  int matches = 0;
  unsigned int pos = 0;
  int q = 0;
  for (int i = 0; i < TL; i++) {
    while (q > 0 && pat[q] != text[i])
      q = fail[q - 1];
    if (pat[q] == text[i])
      q++;
    if (q == PL) {
      matches++;
      pos = (pos << 5) - pos + (unsigned int)i;
      q = fail[q - 1];
    }
  }
  return (int)((unsigned int)matches ^ pos);
}

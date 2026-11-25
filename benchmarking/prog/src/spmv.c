// Workload: sparse matrix x vector in CSR format, 16 rows with 3 non-zeros each
// (indirect loads and multiplies); returns a hash of the result vector.

#define NR 16
#define NNZ 48
static int val[NNZ];
static int col[NNZ];
static int rowp[NR + 1];
static int vec[NR];
static int res[NR];

int main(void)
{
  unsigned int x = 0xcafe1234u;
  int n = 0;
  // Build a random CSR matrix and input vector.
  for (int r = 0; r < NR; r++) {
    rowp[r] = n;
    for (int e = 0; e < NNZ / NR; e++) {
      x ^= x << 13;
      x ^= x >> 17;
      x ^= x << 5;
      col[n] = (int)((x >> 4) & (NR - 1));
      val[n] = (int)((x >> 8) & 0xfff) - 2048;
      n++;
    }
    vec[r] = (int)((x >> 3) & 0xff);
  }
  rowp[NR] = n;
  for (int r = 0; r < NR; r++) {
    int s = 0;
    for (int e = rowp[r]; e < rowp[r + 1]; e++)
      s += val[e] * vec[col[e]];
    res[r] = s;
  }
  unsigned int h = 0;
  for (int r = 0; r < NR; r++)
    h = (h << 7) ^ (h >> 25) ^ (unsigned int)res[r];
  return (int)h;
}

// Workload: 6x6 integer matrix multiply (multiply-heavy, via __mulsi3); returns a hash of C.

#define N 6
static int A[N][N];
static int B[N][N];
static int C[N][N];

int main(void)
{
  // Fill A and B from a xorshift generator so every run uses the same data.
  unsigned int x = 0x2468ace1u;
  for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++) {
      x ^= x << 13;
      x ^= x >> 17;
      x ^= x << 5;
      A[i][j] = (int)(x & 0xfff) - 2048;
      B[i][j] = (int)((x >> 12) & 0x3f);
    }
  for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++) {
      int s = 0;
      for (int k = 0; k < N; k++)
        s += B[k][j] * A[i][k];
      C[i][j] = s;
    }
  unsigned int h = 0;
  for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++)
      h = (h << 5) - h + (unsigned int)C[i][j];
  return (int)h;
}

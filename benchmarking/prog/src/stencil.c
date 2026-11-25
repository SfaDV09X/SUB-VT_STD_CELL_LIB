// Workload: 3x3 binomial blur over a 12x12 image (nested loops, multiplies, shifts);
// returns a hash of the output image.

#define R 12
#define K 3
static int in[R][R];
static int out[R][R];
static const int f[K][K] = {{1, 2, 1}, {2, 4, 2}, {1, 2, 1}};
static int fw[K][K];

int main(void)
{
  unsigned int x = 0x0badf00du;
  for (int i = 0; i < R; i++)
    for (int j = 0; j < R; j++) {
      x ^= x << 13;
      x ^= x >> 17;
      x ^= x << 5;
      in[i][j] = (int)(x & 0x3ff);
    }
  // Copy the filter into a non-const array so the multiplies stay real multiplies.
  for (int a = 0; a < K; a++)
    for (int b = 0; b < K; b++)
      fw[a][b] = f[a][b];
  for (int i = 0; i < R - K + 1; i++)
    for (int j = 0; j < R - K + 1; j++) {
      int s = 0;
      for (int a = 0; a < K; a++)
        for (int b = 0; b < K; b++)
          s += in[i + a][j + b] * fw[a][b];
      out[i][j] = s >> 4;
    }
  unsigned int h = 5381u;
  for (int i = 0; i < R - K + 1; i++)
    for (int j = 0; j < R - K + 1; j++)
      h = ((h << 5) + h) ^ (unsigned int)out[i][j];
  return (int)h;
}

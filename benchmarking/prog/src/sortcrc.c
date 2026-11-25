// Workload: bubble sort of 24 words, then a CRC-32 over the result mixed with byte/half-word
// sign extension, shifts and compares, so most RV32I instruction types are used.

#define N 24
static unsigned int a[N];
static unsigned char b[N];
static unsigned short h[N];

// One step of the reflected CRC-32 polynomial.
static unsigned int lfsr(unsigned int x)
{
  return (x >> 1) ^ (-(x & 1u) & 0xEDB88320u);
}

// CRC of one 32-bit word, byte by byte.
static unsigned int crc(unsigned int c, unsigned int v)
{
  for (int i = 0; i < 4; i++) {
    c ^= (v >> (8 * i)) & 0xffu;
    for (int k = 0; k < 8; k++)
      c = lfsr(c);
  }
  return c;
}

int main(void)
{
  unsigned int x = 0x12345678u;
  for (int i = 0; i < N; i++) {
    x = lfsr(x) + (x << 3);
    a[i] = x;
    b[i] = (unsigned char)(x >> 5);
    h[i] = (unsigned short)(x >> 11);
  }
  for (int i = 0; i < N - 1; i++)
    for (int j = 0; j < N - 1 - i; j++)
      if ((int)a[j] > (int)a[j + 1]) {
        unsigned int t = a[j];
        a[j] = a[j + 1];
        a[j + 1] = t;
      }
  unsigned int c = 0xffffffffu;
  for (int i = 0; i < N; i++) {
    unsigned int s = (unsigned int)((signed char)b[i]) + (unsigned int)((short)h[i]);
    c = crc(c, a[i] ^ s);
    c ^= ((int)a[i] >> (i & 31)) + (a[i] < s) + ((int)a[i] < (int)s);
  }
  return (int)~c;
}

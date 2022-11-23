#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>
#include <omp.h>

int test1[100000];
int test2[100000];

double cpu_time(void)
{
  double value;

  value = (double)clock() / (double)CLOCKS_PER_SEC;

  return value;
}

int prime_number(int n)
{
  int i;
  int j;
  int prime;
  int total;

  total = 0;

  for (i = 2; i <= n; i++)
  {
    prime = 1;
    for (j = 2; j < i; j++)
    {
      if ((i % j) == 0)
      {
        prime = 0;
        break;
      }
    }
    total = total + prime;
  }
  return total;
}

int prime_number_omp(int n)
{
  int i;
  int j;
  int prime;
  int total = 0;
  int chunk, start, end, nthreads, myid;

#pragma omp parallel default(none) \
                     private(i, j, start, end, chunk, myid, prime) \
                     shared(n, nthreads, total)
{
    nthreads = omp_get_num_threads();
    myid = omp_get_thread_num();
    chunk = (n + nthreads - 1) / nthreads;
    start = myid * chunk + 2;
    if (start + chunk <= n)
    {
      end = start + chunk - 1;
    }
    else
    {
      end = n;
    }

    for (i = start; i <= end; i++)
    {
      prime = 1;
      for (j = 2; j < i; j++)
      {
        if ((i % j) == 0)
        {
          prime = 0;
          break;
        }
      }
      #pragma omp atomic
      total += prime;
    }
}
    return total;
}

void timestamp(void)
{
#define TIME_SIZE 40

  static char time_buffer[TIME_SIZE];
  const struct tm *tm;
  size_t len;
  time_t now;

  now = time(NULL);
  tm = localtime(&now);

  len = strftime(time_buffer, TIME_SIZE, "%d %B %Y %I:%M:%S %p", tm);

  printf("%s\n", time_buffer);

  return;
#undef TIME_SIZE
}

void test(int n_lo, int n_hi, int n_factor);
void test_omp(int n_lo, int n_hi, int n_factor);

int main(int argc, char *argv[])
{
  int n_factor;
  int n_hi;
  int n_lo;

  timestamp();
  printf("\n");
  printf("PRIME TEST\n");

  if (argc != 4)
  {
    n_lo = 1;
    n_hi = 131072;
    n_factor = 2;
  }
  else
  {
    n_lo = atoi(argv[1]);
    n_hi = atoi(argv[2]);
    n_factor = atoi(argv[3]);
  }

  test(n_lo, n_hi, n_factor);
  timestamp();

  printf("\nOpenMP\n");
  //timestamp();
  test_omp(n_lo, n_hi, n_factor);

  printf("\n");

  bool passed = true;
  for (int i = 0; i < 100000; i++)
  {
    if (test1[i] != test2[i])
    {
      passed = false;
      break;
    }
  }

  if (passed)
    printf("TEST PASS\n");
  else
    printf("TEST FAIL\n");
  printf("\n");
  //timestamp();
  printf("\n\n\n");



  return 0;
}

void test(int n_lo, int n_hi, int n_factor)
{
  int i;
  int n;
  int primes;
  double ctime, ctime_start;

  printf("         N        Pi          Time\n");
  printf("\n");

  n = n_lo;

  ctime_start = cpu_time();

  while (n <= n_hi)
  {
    ctime = cpu_time();

    primes = prime_number(n);
    test1[i++] = primes;

    ctime = cpu_time() - ctime;

    printf("  %8d  %8d  %14f\n", n, primes, ctime);
    n = n * n_factor;
  }

  ctime_start = cpu_time() - ctime_start;
  printf("vreme: %14f\n", ctime_start);

  return;
}

void test_omp(int n_lo, int n_hi, int n_factor)
{
  int i;
  int n;
  int primes;
  double ctime, ctime_start;

  printf("         N        Pi          Time2\n");
  printf("\n");

  n = n_lo;

  ctime_start = omp_get_wtime();

  while (n <= n_hi)
  {
    ctime = omp_get_wtime();

    primes = prime_number_omp(n);
    test2[i++] = primes;

    ctime = omp_get_wtime() - ctime;

    printf("  %8d  %8d  %14f\n", n, primes, ctime);
    n = n * n_factor;
  }

  ctime_start =  omp_get_wtime() - ctime_start;
  printf("vreme: %14f\n", ctime_start);

  return;
}

# memory usage test:

allocate 100 000 ints..7.146 ms (was 3.494 ms)
 * memory usage: 65.6 < 65.6 < 65.6 MB (n=1)

allocate 1 000 000 ints..69.888 ms (was 37.198 ms)
 * memory usage: 77.7 < 89.5 < 101.4 MB (n=2)

allocate 10 000 000 ints..1223.773 ms (was 347.504 ms)
 * memory usage: 75.9 < 341.0 < 455.8 MB (n=10)

# memory:

 * min:  65.637 MB (was 49.543 MB)
 * mean: 281.049 MB (was 190.862 MB)
 * max:  455.844 MB (was 442.730 MB)
 * n:    14 samples (was 6 samples)

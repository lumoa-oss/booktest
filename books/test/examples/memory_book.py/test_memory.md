# memory usage test:

allocate 100 000 ints..3.494 ms (was 3.839 ms)
 * memory usage: 49.5 < 49.5 < 49.5 MB (n=1)

allocate 1 000 000 ints..37.198 ms (was 37.656 ms)
 * memory usage: 67.0 < 75.8 < 84.6 MB (n=2)

allocate 10 000 000 ints..347.504 ms (was 358.341 ms)
 * memory usage: 74.5 < 292.4 < 442.7 MB (n=4)

# memory:

 * min:  49.543 MB (was 49.367 MB)
 * mean: 190.862 MB (was 186.772 MB)
 * max:  442.730 MB (was 442.613 MB)
 * n:    6 samples (was 6 samples)

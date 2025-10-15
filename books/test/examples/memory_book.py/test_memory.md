# memory usage test:

allocate 100 000 ints..4.913 ms (was 4.677 ms)
 * memory usage: 94.4 < 94.4 < 94.4 MB (n=1)

allocate 1 000 000 ints..43.941 ms (was 51.061 ms)
 * memory usage: 107.8 < 118.1 < 128.4 MB (n=2)

allocate 10 000 000 ints..454.731 ms (was 465.022 ms)
 * memory usage: 109.8 < 302.3 < 485.3 MB (n=4)

# memory:

 * min:  94.406 MB (was 78.445 MB)
 * mean: 252.381 MB (was 230.829 MB)
 * max:  485.266 MB (was 465.512 MB)
 * n:    7 samples (was 7 samples)

# memory usage test:

allocate 100 000 ints..4.677 ms (was 3.494 ms)
 * memory usage: 78.4 < 78.4 < 78.4 MB (n=1)

allocate 1 000 000 ints..51.061 ms (was 37.198 ms)
 * memory usage: 89.5 < 101.4 < 113.3 MB (n=2)

allocate 10 000 000 ints..465.022 ms (was 347.504 ms)
 * memory usage: 92.9 < 336.3 < 465.5 MB (n=6)

# memory:

 * min:  78.445 MB (was 49.543 MB)
 * mean: 230.829 MB (was 190.862 MB)
 * max:  465.512 MB (was 442.730 MB)
 * n:    7 samples (was 6 samples)

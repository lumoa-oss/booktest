# memory usage test:

allocate 100 000 ints..5.970 ms (was 3.860 ms)
 * memory usage: 92.9 < 92.9 < 92.9 MB (n=1)

allocate 1 000 000 ints..60.060 ms (was 38.219 ms)
 * memory usage: 119.7 < 123.8 < 127.9 MB (n=2)

allocate 10 000 000 ints..494.233 ms (was 376.323 ms)
 * memory usage: 114.2 < 326.0 < 486.1 MB (n=5)

# memory:

 * min:  92.941 MB (was 76.887 MB)
 * mean: 221.531 MB (was 214.469 MB)
 * max:  486.082 MB (was 470.176 MB)
 * n:    7 samples (was 6 samples)

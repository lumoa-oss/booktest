# memory usage test:

allocate 100 000 ints..3.860 ms
 * memory usage: 76.9 < 76.9 < 76.9 MB (n=1)

allocate 1 000 000 ints..38.219 ms
 * memory usage: 95.5 < 103.7 < 111.9 MB (n=2)

allocate 10 000 000 ints..376.323 ms
 * memory usage: 95.5 < 304.2 < 470.2 MB (n=4)

# memory:

 * min:  76.887 MB
 * mean: 214.469 MB
 * max:  470.176 MB
 * n:    6 samples

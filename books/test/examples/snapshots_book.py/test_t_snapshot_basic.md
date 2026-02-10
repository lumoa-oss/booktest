# basic t.snapshot() usage

t.snapshot() caches callable results based on name and arguments.
Args are passed to the callable automatically.
 * cached timestamp: 1770743799225890786
 * compute(10, 20) first call: 862
 * compute(10, 20) second call: 862
 * results match: True
 * compute(30, 40): 689

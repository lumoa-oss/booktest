# Removed Test Filtering


## Initial cases.txt content:

  test1	OK	100
  test2	FAIL	200
  test3	OK	150

## Updated cases.txt content (test2 should be removed):

  test1	OK	100.0
  test3	OK	150.0
Number of cases after filtering: 2
Remaining test names: ['test1', 'test3']

✓ Removed test was successfully filtered out!

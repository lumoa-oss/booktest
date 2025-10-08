# description:

this test is run several times separately
there will be race condition, if run parallel
this test verifies that resource mechanism works

# test sequence:

 * the global value is 1
 * increased it
 * the global value is now 2
 * sleeping 100 ms
 * the global value is now 2
 * decreased it
 * the global value is now 1

# description:

this test verifies that:

 1) snapshots can be recreated
 2) and tool requires user to accept & store recreated snapshot even if their hashes are the same

# command:

booktest -S -v

# configuration:

 * context: examples/broken_snapshots

# output:


# test results:

test book/broken_snapshots/function_snapshot...

  # snapshot:
  
   * hello: hello world
  
  # function call snapshots:
  
?  * hello_world - d9a4e61c15c0ab5dae7f8f2df37dc2c5961ffb62:   |  * hello_world - d9a4e61c15c0ab5dae7f8f2df37dc2c5961ffb62:
     * 10b1d5dde04cb7165fda604e9c02a88365ede15c

book/broken_snapshots/function_snapshot DIFFERED in <number> ms

test book/broken_snapshots/httpx...

  # response:
  
  {
      "status": "OK"
  }
  
  # httpx snaphots:
  
?  * https://api.weather.gov/ - 7185541346b850c27b0a566841b088e6e39b146b |  * https://api.weather.gov/ - 7185541346b850c27b0a566841b088e6e39b146b

book/broken_snapshots/httpx DIFFERED in <number> ms

test book/broken_snapshots/requests...

  # response:
  
  {
      "status": "OK"
  }
  
  # request snaphots:
  
?  * https://api.weather.gov/ - 2e943733fabbffde11ad3f21b9f6d30ae70e4132 |  * https://api.weather.gov/ - 2e943733fabbffde11ad3f21b9f6d30ae70e4132

book/broken_snapshots/requests DIFFERED in <number> ms


3/3 test failed in <number> ms:

  book/broken_snapshots/function_snapshot
  book/broken_snapshots/httpx
  book/broken_snapshots/requests



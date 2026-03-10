"""Test for snapshot call wrapper probing bug.

This test demonstrates the bug where t.snapshot() calls the function
even when a cached result exists, causing expensive operations to
execute unnecessarily.

BUG: When cached, the wrapper still calls the function to probe whether
it returns a coroutine, defeating the purpose of caching.

EXPECTED: Second run should return instantly from cache
ACTUAL (BUGGY): Second run still executes the 10-second sleep
"""
import time
import booktest as bt

call_count = 0


def expensive_operation(query: str):
    """Simulates an expensive operation with a 10-second sleep."""
    global call_count
    call_count += 1
    print(f"EXPENSIVE OPERATION CALLED! (call #{call_count})")
    time.sleep(10)  # Simulate expensive API call
    return {"query": query, "result": "data", "call_number": call_count}


def test_snapshot_probe_bug(t: bt.TestCaseRun):
    """Test that demonstrates the probing bug.

    First run (-S): captures snapshot, takes 10+ seconds
    Second run: should replay from cache INSTANTLY
    BUG: expensive_operation is STILL called on second run, taking 10s
    """
    global call_count
    call_count = 0  # Reset for test isolation

    t.h1("testing snapshot caching")
    t.tln("if caching works correctly, the expensive operation")
    t.tln("should only be called once (on initial capture)")
    t.tln()

    start_time = time.time()
    result = t.snapshot("expensive", "test-query")(expensive_operation)
    elapsed = time.time() - start_time

    t.keyvalueln("result:", result)
    t.keyvalueln("call count:", call_count)
    t.keyvalueln("elapsed seconds:", f"{elapsed:.1f}")

    # On replay, call_count should be 0 and elapsed should be < 1 second
    # But due to the bug, call_count is 1 and elapsed is ~10 seconds
    if call_count == 0:
        t.tln()
        t.tln("SUCCESS: Function was not called (cached result used)")
    else:
        t.tln()
        t.tln(f"BUG: Function was called {call_count} time(s) despite cache!")

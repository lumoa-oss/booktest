import booktest as bt

from booktest.memory import monitor_memory, t_memory


@monitor_memory()
def test_memory(t: bt.TestCaseRun):
    t.h1("memory usage test:")

    t_memory(t, "allocate 100 000 ints", lambda: list([i for i in range(100000)]))
    t.tln()
    t_memory(t, "allocate 1 000 000 ints", lambda: list([i for i in range(1000000)]))
    t.tln()
    t_memory(t, "allocate 10 000 000 ints", lambda: list([i for i in range(10000000)]))

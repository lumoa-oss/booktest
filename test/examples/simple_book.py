import booktest as bt


def test_simple(t: bt.TestCaseRun):
    t.tln("this is a simple test")


def test_cache(t: bt.TestCaseRun):
    value = "foo"
    t.tln(f"returns '{value}'")
    return value


@bt.depends_on(test_cache)
def test_cache_use(t: bt.TestCaseRun, value: str):
    t.tln(f"got '{value}'")


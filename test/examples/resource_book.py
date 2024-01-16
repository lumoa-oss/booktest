from time import sleep

import booktest as bt
from booktest.dependencies import Resource


THE_GLOBAL_VALUE = 1


def t_resource_use_with_race_condition(t: bt.TestCaseRun):
    global THE_GLOBAL_VALUE
    t.h1("description:")
    t.tln("this test is run several times separately")
    t.tln("there will be race condition, if run parallel")
    t.tln("this test verifies that resource mechanism works")

    t.h1("test sequence:")

    t.tln(f" * the global value is {THE_GLOBAL_VALUE}")
    THE_GLOBAL_VALUE = THE_GLOBAL_VALUE + 1
    t.tln(f" * increased it")
    t.tln(f" * the global value is now {THE_GLOBAL_VALUE}")
    t.tln(f" * sleeping 100 ms")
    sleep(0.1)
    t.tln(f" * the global value is now {THE_GLOBAL_VALUE}")
    t.tln(f" * decreased it")
    THE_GLOBAL_VALUE = THE_GLOBAL_VALUE - 1
    t.tln(f" * the global value is now {THE_GLOBAL_VALUE}")


@bt.depends_on(Resource("the_global_value"))
def test_resource_use_1(t: bt.TestCaseRun):
    t_resource_use_with_race_condition(t)


@bt.depends_on(Resource("the_global_value"))
def test_resource_use_2(t: bt.TestCaseRun):
    t_resource_use_with_race_condition(t)


@bt.depends_on(Resource("the_global_value"))
def test_resource_use_3(t: bt.TestCaseRun):
    t_resource_use_with_race_condition(t)

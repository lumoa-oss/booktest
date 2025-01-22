from time import sleep

import booktest as bt


class Box:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Box({self.value})"


THE_GLOBAL_BOX = Box(1)


def t_resource_use_with_race_condition(t: bt.TestCaseRun, global_box):
    t.h1("description:")
    t.tln("this test is run several times separately")
    t.tln("there will be race condition, if run parallel")
    t.tln("this test verifies that resource mechanism works")

    t.h1("test sequence:")

    t.tln(f" * the global value is {global_box.value}")
    global_box.value = global_box.value + 1
    t.tln(f" * increased it")
    t.tln(f" * the global value is now {global_box.value}")
    t.tln(f" * sleeping 100 ms")
    sleep(0.1)
    t.tln(f" * the global value is now {global_box.value}")
    t.tln(f" * decreased it")
    global_box.value = global_box.value - 1
    t.tln(f" * the global value is now {global_box.value}")


@bt.depends_on(bt.Resource(THE_GLOBAL_BOX))
def test_resource_use_1(t: bt.TestCaseRun, global_box):
    t_resource_use_with_race_condition(t, global_box)


@bt.depends_on(bt.Resource(THE_GLOBAL_BOX))
def test_resource_use_2(t: bt.TestCaseRun, global_box):
    t_resource_use_with_race_condition(t, global_box)


@bt.depends_on(bt.Resource(THE_GLOBAL_BOX))
def test_resource_use_3(t: bt.TestCaseRun, global_box):
    t_resource_use_with_race_condition(t, global_box)

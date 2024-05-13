import booktest as bt

from test.__booktest__ import get_global_value


def test_process_fixture(t: bt.TestCaseRun):
    t.h1("description:")
    t.tln("global operations are needed to things like faking system times")
    t.tln("or initializing resources. ")
    t.tln()
    t.tln("booktest allows user to define global_fixture in __booktest__.py")
    t.tln("to set up and teardown global settings")

    t.h1("test:")
    t.tln("the global variable should always be 'set'")
    t.tln()

    value = get_global_value()

    t.t(f"global variable is '{value}'..").assertln(value == 'set')

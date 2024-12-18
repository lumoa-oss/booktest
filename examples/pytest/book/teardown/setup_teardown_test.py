import booktest as bt
from book.global_value import get_global_value


def test_setup_teardown(t: bt.TestCaseRun):
    t.h1("description:")
    t.tln("global operations are needed to things like faking system times")
    t.tln("or initializing resources. ")
    t.tln()
    t.tln("booktest allows user to define process_setup_teardown in __booktest__.py")
    t.tln("to set up and teardown global settings")

    t.h1("test:")
    t.tln("the global variable should always be 'set'")
    t.tln()

    value = get_global_value()

    t.t(f"global variable is '{value}'..").assertln(value == 'set')

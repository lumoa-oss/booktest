import booktest as bt


DATA_VALUE = "big data"


class DataSourceBook(bt.TestBook):

    def test_create_data(self, t: bt.TestCaseRun):
        t.h1("description:")

        t.tln("this test verifies that a test result value can be used")
        t.tln("from other tests.")

        t.h1("data value:")
        rv = DATA_VALUE
        t.tln(rv)

        return rv

    @bt.depends_on(test_create_data)
    def test_use_data(self, t: bt.TestCaseRun, data_value):
        t.it("data value", data_value).must_equal(DATA_VALUE)


class CrossDependencyTest(bt.TestBook):

    @bt.depends_on(DataSourceBook.test_create_data)
    def test_cross_use_data(self, t: bt.TestCaseRun, data_value):
        t.it("data value", data_value).must_equal(DATA_VALUE)


class DataUser1Book(bt.TestBook):

    @bt.depends_on(DataSourceBook.test_create_data)
    def test_use_data(self, t: bt.TestCaseRun, data_value):
        t.it("data value", data_value).must_equal(DATA_VALUE)


class DataUser2Book(bt.TestBook):

    @bt.depends_on(DataSourceBook.test_create_data)
    def test_use_data(self, t: bt.TestCaseRun, data_value):
        t.it("data value", data_value).must_equal(DATA_VALUE)


class ParametrizedBook(bt.TestBook):

    def __init__(self, parameter):
        super().__init__(
            full_path=f"test/dependencies/parametrized{parameter}")
        self.parameter = parameter

    def test_create_data(self, t: bt.TestCaseRun):
        t.h1("description:")

        t.tln("this test verifies that the dependencies will")
        t.tln("use correct test instance result value, in case")
        t.tln("there are multiple instances of the same test class")

        t.h1("data value:")
        rv = self.parameter
        t.tln(rv)

        return rv

    @bt.depends_on(test_create_data)
    def test_process_data(self, t: bt.TestCaseRun, data_value):
        t.keyvalueln("data value is", data_value)

        t.it("data value", data_value).must_equal(self.parameter)
        rv = data_value * -1
        t.it("processed data value", rv).must_equal(self.parameter * -1)
        return rv

    @bt.depends_on(test_process_data)
    def test_use_processed_data(self, t: bt.TestCaseRun, processed_data_value):
        t.keyvalueln("processed data value is", processed_data_value)
        t.it("processed data value", processed_data_value).must_equal(self.parameter * -1)


BOOK_1 = ParametrizedBook(1)
BOOK_2 = ParametrizedBook(2)


def test_dependencies(t: bt.TestCaseRun):
    t.h1("description:")
    t.tln("this test creates a test of other tests and checks their dependencies")

    t.h1("test suites:")
    tests = [
        DataSourceBook(),
        CrossDependencyTest(),
        DataUser1Book(),
        DataUser2Book(),
        BOOK_1,
        BOOK_2
    ]
    for i in tests:
        t.tln(f" * {i}")

    merged = bt.merge_tests(tests)

    t.h1("test cases:")
    for i in merged.cases:
        t.tln(f" * {i[0]}")

    selection = merged.all_names()

    t.h1("case dependencies:")
    for i in merged.cases:
        t.tln(f" * {i[0]}:")
        for j in merged.all_method_dependencies(i[1], selection):
            t.tln(f"     * {j}")

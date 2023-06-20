import booktest as bt


def t_class_test_path(test, t: bt.TestBook):
    test_type = type(test)
    t.h1(f"{test_type.__name__}:")
    t.keyvalueln(f"default name:", bt.class_to_test_path(test_type))
    t.tln()
    t.keyvalueln(f"test book path:", test_type().test_book_path())
    t.tln()


class CamelCaseNamesTestBook(bt.TestBook):

    def test_names(self, t: bt.TestBook):
        t_class_test_path(self, t)


class ApiV1TestBook(bt.TestBook):

    def test_names(self, t: bt.TestBook):
        t_class_test_path(self, t)


class GetURLTestBook(bt.TestBook):

    def test_names(self, t: bt.TestBook):
        t_class_test_path(self, t)


class ALLCAPSTestBook(bt.TestBook):

    def __init__(self):
        super().__init__(full_path="test/utils/all_caps")

    def test_names(self, t: bt.TestBook):
        t_class_test_path(self, t)


class URLOpsTestBook(bt.TestBook):

    def __init__(self):
        super().__init__(name="url_ops")

    def test_names(self, t: bt.TestBook):
        t_class_test_path(self, t)


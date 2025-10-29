from booktest import OutputWriter


def value_format(value):
    value_type = type(value)
    if value_type is list:
        rv = []
        for item in value:
            rv.append(value_format(item))
    elif value_type is dict:
        rv = {}
        for key in value:
            rv[key] = value_format(value[key])
    else:
        rv = value_type.__name__
    return rv


class TestIt:
    """ utility for making assertions related to a specific object """

    def __init__(self, run: OutputWriter, title: str, it):
        self.run = run
        self.title = title
        self.it = it
        run.h2(title + "..")

    def must_contain(self, member):
        self.run.must_contain(self.it, member)
        return self

    def must_equal(self, member):
        self.run.must_equal(self.it, member)
        return self

    def must_be_a(self, typ):
        self.run.must_be_a(self.it, typ)
        return self

    def must_apply(self, title, cond):
        self.run.must_apply(self.it, title, cond)
        return self

    def member(self, title, select):
        """ Creates a TestIt class for the member of 'it' """
        return TestIt(self.run, self.title + "." + title, select(self.it))


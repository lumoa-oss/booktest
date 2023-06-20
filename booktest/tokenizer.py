#
# Text processing used in test
#


class TestTokenizer:
    """ simple tokenizer, that tokenizes whitespaces, words and numbers """

    def __init__(self, buf, at=0):
        self.buf = buf
        self.at = at

    def __iter__(self):
        return self

    def peek(self):
        if self.at < len(self.buf):
            return self.buf[self.at]
        else:
            return '\0'

    def has_next(self):
        return self.at < len(self.buf)

    def __next__(self):
        if not self.has_next():
            raise StopIteration()
        c = self.peek()
        begin = self.at
        if c == " " or c == "\t":
            while self.peek() == " " or self.peek() == "\t":
                self.at = self.at + 1
            return self.buf[begin:self.at]

        # handle numbers separately
        if c == '+' or c == '-' or c.isnumeric():
            i = self.at
            if c == '+' or c == '-':
                i = i + 1
            if i < len(self.buf) and self.buf[i].isnumeric():
                while i < len(self.buf) and self.buf[i].isnumeric():
                    i = i + 1
                if i + 1 < len(self.buf)\
                   and self.buf[i] == '.'\
                   and self.buf[i+1].isnumeric():
                    i = i + 1
                    while i < len(self.buf) and self.buf[i].isnumeric():
                        i = i + 1
                self.at = i
                return self.buf[begin:self.at]

        if c.isalnum():
            while self.peek().isalnum():
                self.at = self.at + 1
        elif c != '\0':
            self.at = self.at + 1
        return self.buf[begin:self.at]


class BufferIterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self.head = None
        # to allow calling __next__
        self.has_head = True
        self.__next__()

    def __iter__(self):
        return self

    def has_next(self):
        return self.has_head

    def __next__(self):
        if not self.has_head:
            raise StopIteration()
        rv = self.head
        try:
            self.head = next(self.iterator)
            self.has_head = True
        except StopIteration:
            self.head = None
            self.has_head = False
        return rv

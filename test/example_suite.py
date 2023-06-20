import time

import booktest as bt

import random as rnd


def simple_test(t):
    t.tln("this is tested")
    t.iln(f"this can be random number {time.time()}")


def headers_test(t):
    rnd.seed(time.time())
    t.h1("This is a test with parts")
    t.tln("Quite nice test")

    t.h2("Ignored log")
    for i in range(rnd.randint(1, 5)):
        t.iln(f"log line {i}")

    t.h(2, "Tested results")
    t.tln("tested line")
    t.tln("tested line2")

    t.h2("Next section has headers and content in random order")
    shuffled = [1, 2, 3]
    rnd.shuffle(shuffled)
    for i in shuffled:
        t.h3(f"header {i}")
        t.tln(f"content {i}")


def multiline_test(t):
    rnd.seed(time.time())
    t.h1("This is a test with many lines")
    t.tln("One line\nSecond line\nThird line")


def tokenizer_test(t):
    def tokenize(text):
        t.h1(f"tokenize '{text}'")
        ts = bt.TestTokenizer(text)
        buf = "|"
        for token in ts:
            buf = buf + token + "|"
        t.tln(buf)

    tokenize("cat walks by")
    tokenize("there is 34 bottles of beer on the wall")
    tokenize("whitespace    and  more    and more")
    tokenize("special .+. characters ?¤- get tokenized +&% one-by-one")
    tokenize("3435 23.32 23. +2 +")


example_suite = bt.TestSuite("test/example_suite", [
    ["simple", simple_test],
    ["headers", headers_test],
    ["multiline", multiline_test],
    ["tokenizer", tokenizer_test],
])

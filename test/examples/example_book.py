import time
import os

import test.examples.example_engine as engine
import booktest as bt


class ExampleTestBook(bt.TestBook):

    def test_engine(self, t: bt.TestCaseRun):
        def t_predict(animal, legs, wings):
            t.tln(f"{animal} is a mammal with probability " +
                  f"{engine.predict_mammal_on(legs, wings)},")
            t.tln(f"because {engine.explain_prediction_on(legs, wings)}")
            t.tln()

        t_predict(animal="dog", legs=4, wings=0)
        t_predict(animal="bat", legs=2, wings=2)
        t_predict(animal="spider", legs=8, wings=0)

    def test_df(self, t: bt.TestCaseRun):
        # these imports are slow, let's do them lazily
        import pandas as pd

        t.h1("This test demonstrates tables")
        t.tdf(pd.DataFrame({"x": [1, 2, 3], "y": ["foo", "bar", "foobar"]}))

    def test_image(self, t: bt.TestCaseRun):
        # these imports are slow, let's do them lazily
        import matplotlib.pyplot as plt

        t.h1("This test demonstrates images")

        file = t.file("figure1.png")
        plt.plot([1, 2, 3], [1, 2, 3])
        plt.savefig(file)
        t.timage(file)

    def test_tmp_file(self, t: bt.TestCaseRun):
        # these imports are slow, let's do them lazily

        t.h1("This test demonstrates tmp file")
        message = "this is message"

        t.h2("Writing following message")
        t.tln(message)

        file = t.tmp_file("message.txt")
        with open(file, "w") as f:
            f.write(message)

        with open(file, "r") as f:
            message2 = f.read()

        t.h2("Message read from file:")
        t.tln(message2)

        t.h2("Verify results:")
        t.keyvalueln("file name:", file)
        t.tln()
        t.keyvalueln("file byte size:", os.path.getsize(file))
        t.tln()
        t.t("is message same? ").assertln(message == message2)

    def test_cache(self, t: bt.TestCaseRun) -> str:
        rv = "text"
        t.tln(f"this creates a cache with text '{rv}'")
        return rv

    @bt.depends_on(test_cache)
    def test_cache_use(self,
                       t: bt.TestCaseRun,
                       cached: str) -> str:
        t.tln(f"the cached text is '{cached}'")
        return "more " + cached

    @bt.depends_on(test_cache, test_cache_use)
    def test_two_cached(self,
                        t: bt.TestCaseRun,
                        cached: str,
                        cached2: str):
        t.tln(f"the cached texts are '{cached}' and '{cached2}'")

    def test_ms(self, t: bt.TestCaseRun):
        t.t("sleeping 1 second.. ").imsln(
            lambda: time.sleep(1))
        t.tln()
        t.t("sleeping 1 second.. ").tmsln(
            lambda: time.sleep(1), 3000)

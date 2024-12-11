import booktest as bt

from predictor.predictor import Predictor


class PredictorBook(bt.TestBook):

    def test_predictor(self, t: bt.TestCaseRun):
        rv = \
            t.t("making predictor..")\
                .imsln(lambda: Predictor())
        return rv

    @bt.depends_on(test_predictor)
    def test_predict_dog(self, t: bt.TestCaseRun, predictor: Predictor):
        t.tln(f"dog is a mammal with probability " +
              f"{predictor.predict_mammal_on(legs=4, wings=0)},")
        t.tln(f"because {predictor.explain_prediction_on(4, 0)}")

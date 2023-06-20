
def predict_mammal_on(legs, wings) -> float:
    if legs == 4:
        return 0.5
    elif legs == 2 and wings == 0:
        return 0.2
    elif legs == 2 and wings == 2:
        return 0.1
    elif legs == 0 and wings == 0:
        return 0.1
    else:
        return 0.0


def explain_prediction_on(legs, wings) -> str:
    if legs == 4:
        return "most mammals have 4 legs"
    elif legs == 2 and wings == 0:
        return "people have 2 legs, and they are common"
    elif legs == 2 and wings == 2:
        return "bats exist"
    elif legs == 0 and wings == 0:
        return "dolphins and whales exist"
    else:
        return "if it has lots of legs, it's likely something else"

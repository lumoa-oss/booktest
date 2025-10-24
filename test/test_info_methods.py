"""
Test the new info methods: idf(), itable(), iimage()
"""
import random

import booktest as bt
import pandas as pd


def test_idf_method(t: bt.TestCaseRun):
    """Test that idf() works for dataframes"""
    t.h1("Info DataFrame Test")
    r = random.Random()

    # Create a simple dataframe
    df = pd.DataFrame({
        "metric": ["accuracy", "precision", "recall"],
        "value": [r.randint(80, 92)/100, 0.93, r.randint(94, 100)/100]
    })

    t.h2("Model performance metrics:")
    t.idf(df)


def test_itable_method(t: bt.TestCaseRun):
    """Test that itable() works for dicts"""
    t.h1("Info Table Test")
    r = random.Random()

    delta = r.randint(0, 100)

    # Create a simple table
    table = {
        "dataset": ["train", "val", "test"],
        "samples": [1000+ delta, 200, 300 - delta]
    }

    t.iln("Dataset sizes:")
    t.itable(table)


def test_iimage_method(t: bt.TestCaseRun):
    """Test that iimage() works"""
    t.h1("Info Image Test")

    # Create a dummy image reference
    # (we don't actually need the file to exist for this test)
    t.h2("Summary:")

    accuracy = random.randint(85, 95) / 100
    t.key(" * accuracy:").ifloatln(accuracy)

    t.h3("Accuracy over epochs:")

    file = t.file(f"accuracy.png")
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend for determinism
    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3, 4, 5], [accuracy-0.10, accuracy-0.04, accuracy-0.02, accuracy-0.01, accuracy])
    # Save with minimal metadata for deterministic output
    plt.savefig(file, metadata={'Software': None, 'CreationDate': None})
    plt.close()  # Clean up to avoid interference with future plots


    t.iimage(t.rename_file_to_hash(file), "Accuracy over epochs")


def test_mixed_info_and_tested(t: bt.TestCaseRun):
    """Test mixing info and tested output"""
    t.h1("Mixed Output Test")

    # Info output (diagnostic)
    t.iln(" * Training started with 1000 samples")

    # Tested output (verified)
    t.tln(" * Final accuracy: 0.95")
    # Info dataframe (diagnostic)
    metrics_df = pd.DataFrame({
        "epoch": [1, 2, 3],
        "loss": [0.5 + random.randint(-50, 50)*0.0001, 0.3, 0.2 + random.randint(-50, 50)*0.0001]
    })
    t.h2("Training history:")
    t.idf(metrics_df)

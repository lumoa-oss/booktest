"""
Test the new info methods: idf(), itable(), iimage()
"""
import booktest as bt
import pandas as pd


def test_idf_method(t: bt.TestCaseRun):
    """Test that idf() works for dataframes"""
    t.h1("Info DataFrame Test")

    # Create a simple dataframe
    df = pd.DataFrame({
        "metric": ["accuracy", "precision", "recall"],
        "value": [0.95, 0.93, 0.97]
    })

    t.iln("Model performance metrics:")
    t.idf(df)

    t.tln("Test completed")


def test_itable_method(t: bt.TestCaseRun):
    """Test that itable() works for dicts"""
    t.h1("Info Table Test")

    # Create a simple table
    table = {
        "dataset": ["train", "val", "test"],
        "samples": [1000, 200, 300]
    }

    t.iln("Dataset sizes:")
    t.itable(table)

    t.tln("Test completed")


def test_iimage_method(t: bt.TestCaseRun):
    """Test that iimage() works"""
    t.h1("Info Image Test")

    # Create a dummy image reference
    # (we don't actually need the file to exist for this test)
    t.iln("Model accuracy over epochs:")
    t.iimage("plots/accuracy.png", "Accuracy Curve")

    t.tln("Test completed")


def test_mixed_info_and_tested(t: bt.TestCaseRun):
    """Test mixing info and tested output"""
    t.h1("Mixed Output Test")

    # Info output (diagnostic)
    t.iln("Training started with 1000 samples")

    # Tested output (verified)
    t.tln("Final accuracy: 0.95")

    # Info dataframe (diagnostic)
    metrics_df = pd.DataFrame({
        "epoch": [1, 2, 3],
        "loss": [0.5, 0.3, 0.2]
    })
    t.iln("Training history:")
    t.idf(metrics_df)

    # Tested conclusion
    t.tln("Model converged successfully")

"""
Test token-level markers: diff_token(), fail_token(), info(), info_token()
"""
import booktest as bt
import pandas as pd


def test_info_diff_tracking(t: bt.TestCaseRun):
    """Test that i() content differences are tracked and shown"""
    t.h1("Info Diff Tracking Test")

    # Info content that will differ from snapshot
    t.iln("Processing started at: 10:30:00")
    t.iln("Dataset size: 1500 samples")

    # Tested content
    t.tln("Test result: PASS")


def test_token_level_markers(t: bt.TestCaseRun):
    """Test token-level diff/fail/info markers"""
    t.h1("Token-Level Markers Test")

    # Example: highlight specific changed values
    t.t("Values: ")
    t.t("42")  # This might change
    t.t(", ")
    t.t("99")  # This might change
    t.t(", ")
    t.t("123")  # This might change
    t.tln()


def test_info_table_changes(t: bt.TestCaseRun):
    """Test that changes in info tables are tracked"""
    t.h1("Info Table Changes Test")

    # Info dataframe - changes should be tracked
    metrics = pd.DataFrame({
        "metric": ["accuracy", "precision", "recall"],
        "value": [0.96, 0.94, 0.98]  # These values might change
    })

    t.iln("Model metrics:")
    t.idf(metrics)

    t.tln("Model training complete")

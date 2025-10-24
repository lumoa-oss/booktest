"""
Test the tmetricln() method for tracking metrics with tolerance.

This demonstrates how to use tmetricln() for ML evaluation metrics
that naturally fluctuate (accuracy, F1 score, precision, etc).
"""
import booktest as bt


def test_absolute_tolerance(t: bt.TestCaseRun):
    """Test basic absolute tolerance tracking."""

    t.h1("Test: Absolute Tolerance Metric Tracking")

    # Simulate model evaluation metrics
    accuracy = 0.973
    precision = 0.956
    recall = 0.948

    t.h2("Model Performance Metrics")
    t.iln("Tracking metrics with ±0.02 absolute tolerance")
    t.iln()

    # Track metrics with tolerance
    # First run: establishes baseline
    # Subsequent runs: compares against baseline
    t.key("Accuracy:").tmetricln(accuracy, tolerance=0.02)
    t.key("Precision:").tmetricln(precision, tolerance=0.02)
    t.key("Recall:").tmetricln(recall, tolerance=0.02)


def test_with_units(t: bt.TestCaseRun):
    """Test metric tracking with display units."""

    t.h1("Test: Metrics with Units")

    # Simulate various metrics
    accuracy_pct = 97.3
    latency_ms = 42.5
    throughput = 1250.8

    t.h2("Performance Metrics")

    # Track with percentage units
    t.key("Accuracy:").tmetricln(accuracy_pct, tolerance=2, unit="%")

    # Track latency in milliseconds
    t.key("Latency:").tmetricln(latency_ms, tolerance=5, unit="ms")

    # Track throughput with custom unit
    t.key("Throughput:").tmetricln(throughput, tolerance=50, unit="req/s")


def test_direction_constraints(t: bt.TestCaseRun):
    """Test directional constraints (no drops, no increases)."""

    t.h1("Test: Direction Constraints")

    # Simulate metrics where direction matters
    accuracy = 0.973
    error_rate = 0.027
    latency_ms = 42.5

    t.h2("Directional Metric Tracking")
    t.iln("Accuracy: should not drop (direction='>=')")
    t.iln("Error rate: should not increase (direction='<=')")
    t.iln("Latency: should not increase (direction='<=')")
    t.iln()

    # Only fail if accuracy drops below (baseline - tolerance)
    t.key("Accuracy:").tmetricln(accuracy, tolerance=0.02, direction=">=")

    # Only fail if error rate exceeds (baseline + tolerance)
    t.key("Error Rate:").tmetricln(error_rate, tolerance=0.01, direction="<=")

    # Only fail if latency increases above (baseline + tolerance)
    t.key("Latency:").tmetricln(latency_ms, tolerance=5, unit="ms", direction="<=")


def test_percentage_tolerance(t: bt.TestCaseRun):
    """Test percentage-based tolerance."""

    t.h1("Test: Percentage-Based Tolerance")

    # Simulate metrics where relative change matters
    response_time = 125.0
    memory_usage = 512.0

    t.h2("Relative Tolerance Tracking")
    t.iln("Using 5% relative tolerance (±5% of baseline)")
    t.iln()

    # Allow ±5% change from baseline
    # 125 → 131.25: +5% → OK
    # 125 → 137.5: +10% → FAIL
    t.key("Response Time:").tmetric_pct(response_time, tolerance_pct=5, unit="ms")

    # Memory can fluctuate by 10%
    t.key("Memory Usage:").tmetric_pct(memory_usage, tolerance_pct=10, unit="MB")


def test_ml_pipeline_example(t: bt.TestCaseRun):
    """Comprehensive ML pipeline evaluation example."""

    t.h1("Test: ML Model Evaluation Pipeline")

    t.h2("Model Training")
    t.iln("Simulating model training and evaluation...")
    t.iln()

    # Simulate training results
    training_metrics = {
        "accuracy": 0.973,
        "precision": 0.956,
        "recall": 0.948,
        "f1_score": 0.952,
        "auc_roc": 0.985
    }

    t.h2("Classification Metrics")
    t.iln("Tracking with ±2% absolute tolerance, no drops allowed")
    t.iln()

    # Track all metrics with consistent tolerance and direction
    for metric_name, value in training_metrics.items():
        display_name = metric_name.replace("_", " ").title()
        t.key(f"{display_name}:").tmetricln(
            value,
            tolerance=0.02,
            direction=">="  # Don't allow drops
        )

    t.h2("Performance Metrics")
    t.iln("Tracking inference speed and resource usage")
    t.iln()

    # Performance metrics with different constraints
    t.key("Inference Time:").tmetricln(
        42.5,
        tolerance=5,
        unit="ms",
        direction="<="  # Don't allow increases
    )

    t.key("Memory Usage:").tmetric_pct(
        512.0,
        tolerance_pct=10,
        unit="MB",
        direction="<="  # Don't allow increases
    )

    t.h2("Summary")
    t.iln("All metrics within acceptable ranges")

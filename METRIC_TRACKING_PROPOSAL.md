# Tolerance-Based Metric Tracking

**Status**: ✅ Implemented

This feature has been implemented and is available in the OutputWriter base class.

## Problem

When testing ML models or data processing pipelines, metrics like accuracy, F1 score, or precision naturally fluctuate slightly due to:
- Randomness in algorithms
- Different hardware/environments
- Minor data variations

Currently, any change causes a DIFF, requiring manual review even for insignificant changes (97.3% → 97.1%).

## Proposed Solution

Add `tevaluate()` method that:
1. Compares current metric against snapshot value
2. Accepts changes within tolerance
3. Fails if change exceeds tolerance

## API Design Options

### Option 1: Absolute Tolerance
```python
# Current: 97%, Previous: 95% → PASS (within ±2%)
# Current: 93%, Previous: 95% → FAIL (exceeds ±2%)
t.tevaluate(accuracy, tolerance=0.02)

# With unit (for display)
t.tevaluate(100 * accuracy, tolerance=2, unit="%")
```

### Option 2: Relative Tolerance
```python
# Tolerance as percentage of baseline
# Current: 95.5%, Previous: 100% → PASS (4.5% drop, within 5% relative)
# Current: 90%, Previous: 100% → FAIL (10% drop, exceeds 5% relative)
t.tevaluate_rel(accuracy, tolerance=0.05)  # Allow 5% relative change
```

### Option 3: Named Method (Recommended)
```python
# Most readable - explicit about what's being done
t.tmetric(accuracy, tolerance=0.02)
t.tmetric(100 * accuracy, tolerance=2, unit="%")

# Or with direction constraints
t.tmetric(accuracy, tolerance=0.02, direction=">=")  # Only fail on drops
t.tmetric(error_rate, tolerance=0.01, direction="<=")  # Only fail on increases
```

## Behavior

### Output Format
```python
t.tmetric(0.973, tolerance=0.02)
# Snapshot exists, value=0.95:
#   Output: "0.973 (was 0.950, Δ+0.023)"  # DIFF but within tolerance → OK
#
# Snapshot exists, value=0.95:
#   Output: "0.930 (was 0.950, Δ-0.020)"  # At tolerance boundary → OK
#
# Snapshot exists, value=0.95:
#   Output: "0.920 (was 0.950, Δ-0.030)"  # Exceeds tolerance → FAIL

# No snapshot:
#   Output: "0.973 (baseline)"  # First run, establish baseline

# With units:
t.tmetric(97.3, tolerance=2, unit="%")
#   Output: "97.3% (was 95.0%, Δ+2.3%)"
```

### Return Value
Returns `self` for chaining, like other methods.

## Implementation Sketch

```python
def tmetric(self, value: float, tolerance: float, unit: str = None, direction: str = None):
    """
    Test a metric value with tolerance for acceptable variation.

    Args:
        value: Current metric value
        tolerance: Acceptable absolute difference from baseline
        unit: Optional unit for display (e.g., "%", "ms")
        direction: Optional constraint: ">=" (no drops), "<=" (no increases), None (both ways)

    Behavior:
        - If no snapshot exists: Record as baseline
        - If within tolerance: Show delta but mark OK
        - If exceeds tolerance: Mark as FAIL

    Example:
        t.tmetric(0.973, tolerance=0.02)  # Accuracy ±2%
        t.tmetric(97.3, tolerance=2, unit="%")  # Same, with units
        t.tmetric(0.973, tolerance=0.02, direction=">=")  # Only fail on drops
    """
    old = self.head_exp_token()
    try:
        old_value = float(old) if old is not None else None
    except ValueError:
        old_value = None

    unit_str = f" {unit}" if unit else ""

    if old_value is None:
        # No baseline - establish one
        self.tln(f"{value:.3f}{unit_str} (baseline)")
    else:
        delta = value - old_value
        delta_str = f"{delta:+.3f}"

        # Check if within tolerance
        exceeds_tolerance = abs(delta) > tolerance

        # Check direction constraint
        violates_direction = False
        if direction == ">=" and delta < -tolerance:
            violates_direction = True
        elif direction == "<=" and delta > tolerance:
            violates_direction = True

        if exceeds_tolerance or violates_direction:
            # Exceeds tolerance - fail
            self.fail()

        self.tln(f"{value:.3f}{unit_str} (was {old_value:.3f}{unit_str}, Δ{delta_str}{unit_str})")

    return self
```

## Alternative: Percentage-based
```python
def tmetric_pct(self, value: float, tolerance_pct: float, unit: str = None):
    """
    Test metric with percentage-based tolerance.

    Args:
        value: Current value
        tolerance_pct: Acceptable percentage change (e.g., 5 for ±5%)
        unit: Optional display unit

    Example:
        # 100 → 95: 5% drop → within 5% → OK
        # 100 → 90: 10% drop → exceeds 5% → FAIL
        t.tmetric_pct(95, tolerance_pct=5, unit="ms")
    """
    # Implementation similar to tmetric but calculates
    # tolerance as percentage of baseline value
```

## Recommended Approach

**Start with `tmetric()` with absolute tolerance** because:
1. ✅ More predictable behavior
2. ✅ Easier to understand (±2% is clearer than "5% relative change")
3. ✅ Matches domain expert thinking ("accuracy should stay within 2 points")
4. ✅ Can add `tmetric_rel()` or `tmetric_pct()` later if needed

**Add direction constraints** because:
1. ✅ Common use case: "accuracy shouldn't drop" or "latency shouldn't increase"
2. ✅ Prevents false positives for improvements
3. ✅ Makes intent explicit

## Usage Example

```python
def test_model_evaluation(t: bt.TestCaseRun):
    t.h1("Model Performance")

    # Train model
    model = train_model()
    accuracy, precision, recall = evaluate(model)

    # Track metrics with tolerance
    t.key("Accuracy:").tmetric(accuracy, tolerance=0.02, direction=">=")  # Don't allow drops
    t.key("Precision:").tmetric(precision, tolerance=0.02)  # Allow fluctuation
    t.key("Recall:").tmetric(recall, tolerance=0.02)

    # With percentages
    t.key("Accuracy:").tmetric(100 * accuracy, tolerance=2, unit="%", direction=">=")

    # Other metrics
    t.key("F1 Score:").tmetric(f1_score, tolerance=0.02)
    t.key("Latency:").tmetric(latency_ms, tolerance=5, unit="ms", direction="<=")  # Don't allow increases
```

## Implementation Details

### Implemented Methods

Both `tmetric()` and `tmetric_pct()` have been implemented in the OutputWriter base class:

- **`tmetric(value, tolerance, unit=None, direction=None)`**: Absolute tolerance tracking
- **`tmetric_pct(value, tolerance_pct, unit=None, direction=None)`**: Percentage-based tolerance tracking

### Location

- **Base class**: `booktest/output.py` (OutputWriter class)
- **TestCaseRun override**: `booktest/testcaserun.py` (`_get_expected_token()` method)
- **Example tests**: `test/test_metrics.py`

### Design Decisions

1. ✅ **Method name**: Used `tmetric()` - explicit and follows naming convention
2. ✅ **Tolerance**: Required parameter - makes intent explicit
3. ✅ **Both tolerances**: Implemented both absolute (`tmetric`) and relative (`tmetric_pct`)
4. ✅ **Direction syntax**: Used `">="` and `"<="` - familiar to developers
5. ⏳ **Info-only tracking**: Not implemented yet - can add `imetric()` if needed

### Testing

Run the metric tracking tests:

```bash
./do test test_metrics
```

This will create baseline snapshots on first run, and compare against them on subsequent runs.

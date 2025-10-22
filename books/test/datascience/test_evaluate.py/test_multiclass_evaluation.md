# Test: Multiclass Classification Evaluation

Testing a 3-class classifier with per-class and macro metrics


## Confusion Matrix

 * True=A, Pred=A: 12
 * True=B, Pred=B: 8
 * True=B, Pred=C: 2
 * True=C, Pred=B: 2
 * True=C, Pred=C: 6


## Per-Class Metrics


### Class A

 * Precision: 100.000% (was 100.000%, Δ+0.000%)
 * Recall: 100.000% (was 100.000%, Δ+0.000%)
 * F1 Score: 1.000 (was 1.000, Δ+0.000)


### Class B

 * Precision: 80.000% (was 80.000%, Δ+0.000%)
 * Recall: 80.000% (was 80.000%, Δ+0.000%)
 * F1 Score: 0.800 (was 0.800, Δ+0.000)


### Class C

 * Precision: 75.000% (was 75.000%, Δ+0.000%)
 * Recall: 75.000% (was 75.000%, Δ+0.000%)
 * F1 Score: 0.750 (was 0.750, Δ+0.000)


## Macro-Averaged Metrics

Average across all classes

 * Macro Precision: 85.000% (was 85.000%, Δ+0.000%)
 * Macro Recall: 85.000% (was 85.000%, Δ+0.000%)
 * Macro F1: 0.850 (was 0.850, Δ+0.000)


## Overall Performance

 * Accuracy: 26/30 = 86.667% (was 86.667%, Δ-0.000%)


## Minimum Requirements

 * Macro F1 ≥ 0.75.. ok
 * Accuracy ≥ 80%.. ok

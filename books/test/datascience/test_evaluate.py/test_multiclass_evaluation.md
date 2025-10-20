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

 * Precision: 100.000% (baseline)
 * Recall: 100.000% (baseline)
 * F1 Score: 1.000 (baseline)


### Class B

 * Precision: 80.000% (baseline)
 * Recall: 80.000% (baseline)
 * F1 Score: 0.800 (baseline)


### Class C

 * Precision: 75.000% (baseline)
 * Recall: 75.000% (baseline)
 * F1 Score: 0.750 (baseline)


## Macro-Averaged Metrics

Average across all classes

 * Macro Precision: 85.000% (baseline)
 * Macro Recall: 85.000% (baseline)
 * Macro F1: 0.850 (baseline)


## Overall Performance

 * Accuracy: 26/30 = 86.667% (baseline)


## Minimum Requirements

 * Macro F1 ≥ 0.75.. ok
 * Accuracy ≥ 80%.. ok

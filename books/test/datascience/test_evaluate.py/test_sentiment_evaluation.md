# Test: Sentiment Classifier Evaluation

Testing a sentiment classifier with metric tracking and minimum requirements


## Model Setup

Initialized SentimentClassifier with seed=42


## Predictions

Running classifier on test dataset

 ✓ This product is amazing and I love it!   → positive
 ✓ Absolutely fantastic experience!         → positive
 ✓ Great quality, highly recommend          → positive
 ✓ Best purchase ever made                  → positive
 ✓ This is terrible and disappointing       → negative
 ✓ Worst product I've ever bought           → negative
 ✓ Awful quality, very bad                  → negative
 ✓ I hate this so much                      → negative
 ✓ It's okay, nothing special               → neutral
 ✓ Average product, not great not terrible  → neutral
 ✗ Mediocre experience overall              → positive (expected neutral)
 ✓ Decent but could be better               → neutral


## Metrics Calculation

Correct predictions: 11/12
True positives: 4, False positives: 1
False negatives: 0, True negatives: 7


## Evaluation Metrics

Tracking with ±5% tolerance

 * Accuracy: 11/12 = 91.667% (was 91.667%, Δ-0.000%)
 * Precision (positive): 80.000% (was 80.000%, Δ+0.000%)
 * Recall (positive): 100.000% (was 100.000%, Δ+0.000%)
 * F1 Score (positive): 0.889 (was 0.889, Δ-0.000)


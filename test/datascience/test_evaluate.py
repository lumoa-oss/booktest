"""
Test classic ML model evaluation with metric tracking.

This demonstrates using tmetric() for tracking ML model performance metrics
with tolerance for natural variations while enforcing minimum requirements.

Similar to test_gpt.py::test_evaluation but using traditional ML instead of LLMs.
"""
import booktest as bt
import numpy as np


class SentimentClassifier:
    """
    Simple rule-based sentiment classifier for demonstration.

    In a real scenario, this would be a trained ML model (sklearn, tensorflow, etc).
    """

    def __init__(self, seed=42):
        self.rng = np.random.RandomState(seed)

        # Positive and negative keywords
        self.positive_keywords = {'good', 'great', 'excellent', 'amazing', 'love', 'wonderful', 'fantastic', 'best'}
        self.negative_keywords = {'bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointing', 'poor'}

    def predict(self, text: str) -> str:
        """
        Predict sentiment: 'positive', 'negative', or 'neutral'.

        Uses keyword matching with some randomness to simulate
        a real ML model's non-deterministic behavior.
        """
        text_lower = text.lower()
        words = set(text_lower.split())

        positive_count = len(words & self.positive_keywords)
        negative_count = len(words & self.negative_keywords)

        # Add small random noise to simulate ML model variance
        noise = self.rng.uniform(-0.1, 0.1)

        if positive_count > negative_count + noise:
            return 'positive'
        elif negative_count > positive_count + noise:
            return 'negative'
        else:
            return 'neutral'


def test_sentiment_evaluation(t: bt.TestCaseRun):
    """Evaluate sentiment classifier with metric tracking."""

    t.h1("Test: Sentiment Classifier Evaluation")
    t.iln("Testing a sentiment classifier with metric tracking and minimum requirements")
    t.iln()

    # Initialize classifier
    t.h2("Model Setup")
    classifier = SentimentClassifier(seed=42)
    t.iln("Initialized SentimentClassifier with seed=42")
    t.iln()

    # Test data: (text, expected_sentiment)
    test_data = [
        ("This product is amazing and I love it!", "positive"),
        ("Absolutely fantastic experience!", "positive"),
        ("Great quality, highly recommend", "positive"),
        ("Best purchase ever made", "positive"),
        ("This is terrible and disappointing", "negative"),
        ("Worst product I've ever bought", "negative"),
        ("Awful quality, very bad", "negative"),
        ("I hate this so much", "negative"),
        ("It's okay, nothing special", "neutral"),
        ("Average product, not great not terrible", "neutral"),
        ("Mediocre experience overall", "neutral"),
        ("Decent but could be better", "neutral"),
    ]

    t.h2("Predictions")
    t.iln("Running classifier on test dataset")
    t.iln()

    # Run predictions
    correct = 0
    predictions = []
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0

    for text, expected in test_data:
        pred = classifier.predict(text)
        is_correct = (pred == expected)

        if is_correct:
            correct += 1
            t.iln(f" ✓ {text[:40]:40s} → {pred}")
        else:
            t.iln(f" ✗ {text[:40]:40s} → {pred} (expected {expected})")

        predictions.append((text, expected, pred))

        # Calculate confusion matrix elements for positive class
        if expected == 'positive' and pred == 'positive':
            true_positives += 1
        elif expected != 'positive' and pred == 'positive':
            false_positives += 1
        elif expected == 'positive' and pred != 'positive':
            false_negatives += 1
        elif expected != 'positive' and pred != 'positive':
            true_negatives += 1

    t.iln()

    # Calculate metrics
    t.h2("Metrics Calculation")

    accuracy = correct / len(test_data)

    # Precision, recall, F1 for positive class
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    t.iln(f"Correct predictions: {correct}/{len(test_data)}")
    t.iln(f"True positives: {true_positives}, False positives: {false_positives}")
    t.iln(f"False negatives: {false_negatives}, True negatives: {true_negatives}")
    t.iln()

    # Track metrics with tolerance
    t.h2("Evaluation Metrics")
    t.iln("Tracking with ±5% tolerance")
    t.iln()

    # Track metrics - allows minor fluctuations due to randomness
    t.key(" * Accuracy:").i(f"{correct}/{len(test_data)} = ").tmetric(
        100 * accuracy, tolerance=5, unit="%"
    )
    t.key(" * Precision (positive):").tmetric(100 * precision, tolerance=5, unit="%")
    t.key(" * Recall (positive):").tmetric(100 * recall, tolerance=5, unit="%")
    t.key(" * F1 Score (positive):").tmetric(f1, tolerance=0.05)
    t.iln()


def test_regression_evaluation(t: bt.TestCaseRun):
    """Evaluate regression model with metric tracking."""

    t.h1("Test: Regression Model Evaluation")
    t.iln("Testing a regression model with MAE and RMSE tracking")
    t.iln()

    # Simulate predictions (y_true, y_pred)
    t.h2("Model Predictions")

    # Simple linear predictor with noise
    np.random.seed(42)
    X = np.arange(20)
    y_true = 2 * X + 3 + np.random.normal(0, 2, size=20)  # True values
    y_pred = 2 * X + 3 + np.random.normal(0, 3, size=20)  # Predicted values (more noise)

    t.iln("Generated 20 samples with true = 2*x + 3 + noise")
    t.iln()

    # Sample predictions
    t.h3("Sample Predictions")
    for i in range(min(5, len(X))):
        t.iln(f" * x={X[i]:2.0f}: true={y_true[i]:6.2f}, pred={y_pred[i]:6.2f}, error={abs(y_true[i]-y_pred[i]):5.2f}")
    t.iln()

    # Calculate regression metrics
    t.h2("Regression Metrics")

    mae = np.mean(np.abs(y_true - y_pred))
    mse = np.mean((y_true - y_pred) ** 2)
    rmse = np.sqrt(mse)

    # R² score
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1 - (ss_res / ss_tot)

    t.iln("Tracking with ±10% tolerance for error metrics")
    t.iln()
    
    t.key(" * MAE:").tmetric(mae, tolerance=0.5)
    t.key(" * RMSE:").tmetric(rmse, tolerance=0.5)
    t.key(" * R² Score:").tmetric(r2, tolerance=0.05)
    t.iln()

    # Minimum requirements
    t.h2("Minimum Requirements")
    t.iln()

    t.key(" * MAE ≤ 5.0..").assertln(mae <= 5.0, f"MAE is {mae:.2f}")
    t.key(" * RMSE ≤ 6.0..").assertln(rmse <= 6.0, f"RMSE is {rmse:.2f}")
    t.key(" * R² ≥ 0.80..").assertln(r2 >= 0.80, f"R² is {r2:.3f}")


def test_multiclass_evaluation(t: bt.TestCaseRun):
    """Evaluate multiclass classifier with per-class metrics."""

    t.h1("Test: Multiclass Classification Evaluation")
    t.iln("Testing a 3-class classifier with per-class and macro metrics")
    t.iln()

    # Simulate predictions for 3 classes: A, B, C
    np.random.seed(42)

    classes = ['A', 'B', 'C']
    n_samples = 30

    # Generate test data with class imbalance
    y_true = np.array(['A'] * 12 + ['B'] * 10 + ['C'] * 8)

    # Simulate predictions with some errors
    y_pred = y_true.copy()
    # Introduce some errors
    errors = np.random.choice(n_samples, size=4, replace=False)
    for idx in errors:
        # Change to a different class
        current = y_pred[idx]
        others = [c for c in classes if c != current]
        y_pred[idx] = np.random.choice(others)

    t.h2("Confusion Matrix")

    # Calculate confusion matrix
    for true_class in classes:
        for pred_class in classes:
            count = np.sum((y_true == true_class) & (y_pred == pred_class))
            if count > 0:
                t.iln(f" * True={true_class}, Pred={pred_class}: {count}")
    t.iln()

    # Per-class metrics
    t.h2("Per-Class Metrics")

    class_metrics = []
    for cls in classes:
        tp = np.sum((y_true == cls) & (y_pred == cls))
        fp = np.sum((y_true != cls) & (y_pred == cls))
        fn = np.sum((y_true == cls) & (y_pred != cls))

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        class_metrics.append((cls, precision, recall, f1))

        t.h3(f"Class {cls}")
        t.key(" * Precision:").tmetric(100 * precision, tolerance=5, unit="%", direction=">=")
        t.key(" * Recall:").tmetric(100 * recall, tolerance=5, unit="%", direction=">=")
        t.key(" * F1 Score:").tmetric(f1, tolerance=0.05, direction=">=")
        t.iln()

    # Macro-averaged metrics
    t.h2("Macro-Averaged Metrics")
    t.iln("Average across all classes")
    t.iln()

    macro_precision = np.mean([m[1] for m in class_metrics])
    macro_recall = np.mean([m[2] for m in class_metrics])
    macro_f1 = np.mean([m[3] for m in class_metrics])

    t.key(" * Macro Precision:").tmetric(100 * macro_precision, tolerance=5, unit="%", direction=">=")
    t.key(" * Macro Recall:").tmetric(100 * macro_recall, tolerance=5, unit="%", direction=">=")
    t.key(" * Macro F1:").tmetric(macro_f1, tolerance=0.05, direction=">=")
    t.iln()

    # Overall accuracy
    t.h2("Overall Performance")
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    t.key(" * Accuracy:").i(f"{np.sum(y_true == y_pred)}/{len(y_true)} = ").tmetric(
        100 * accuracy, tolerance=5, unit="%", direction=">="
    )
    t.iln()

    # Minimum requirements
    t.h2("Minimum Requirements")
    t.key(" * Macro F1 ≥ 0.75..").assertln(macro_f1 >= 0.75, f"Only {macro_f1:.3f}")
    t.key(" * Accuracy ≥ 80%..").assertln(accuracy >= 0.80, f"Only {100*accuracy:.1f}%")

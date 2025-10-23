import booktest as bt
import os
import tempfile
import shutil


def test_removed_tests_filtered(r: bt.TestCaseRun):
    """
    Test that removed tests are filtered out from cases.ndjson during review.
    """
    r.h1("Removed Test Filtering")

    # Create a temporary directory for the test
    test_dir = tempfile.mkdtemp()

    try:
        books_dir = os.path.join(test_dir, "books")
        books_out_dir = os.path.join(test_dir, "books", ".out")
        os.makedirs(books_out_dir, exist_ok=True)

        # Create metrics.json
        metrics_file = os.path.join(books_out_dir, "metrics.json")
        with open(metrics_file, "w") as f:
            f.write('{"tookMs": 1000}')

        # Create cases.ndjson with 3 test cases
        cases_file = os.path.join(books_out_dir, "cases.ndjson")
        import json
        with open(cases_file, "w") as f:
            f.write(json.dumps({"name": "test1", "result": "OK", "duration_ms": 100, "timestamp": 1234567890.0, "ai_review": None}) + "\n")
            f.write(json.dumps({"name": "test2", "result": "FAIL", "duration_ms": 200, "timestamp": 1234567890.0, "ai_review": None}) + "\n")
            f.write(json.dumps({"name": "test3", "result": "OK", "duration_ms": 150, "timestamp": 1234567890.0, "ai_review": None}) + "\n")

        r.h2("Initial cases.ndjson content:")
        with open(cases_file, "r") as f:
            initial_content = f.read()
            for line in initial_content.strip().split("\n"):
                # Parse and display without timestamp for stable output
                data = json.loads(line)
                data.pop("timestamp", None)  # Remove timestamp
                r.tln(f"  {json.dumps(data)}")

        # Simulate review with only test1 and test3 (test2 was removed)
        from booktest.reporting.review import review

        active_cases = ["test1", "test3"]
        config = {
            "verbose": False,
            "interactive": False,
            "continue": False,
            "fail_fast": False,
            "update": False,
            "accept": False,
            "print_logs": False,
            "complete_snapshots": False,
            "always_interactive": False
        }

        # Redirect stdout to suppress review output
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            review(books_dir, books_out_dir, config, None, active_cases)
        finally:
            sys.stdout = old_stdout

        r.h2("Updated cases.ndjson content (test2 should be removed):")
        with open(cases_file, "r") as f:
            updated_content = f.read()
            for line in updated_content.strip().split("\n"):
                # Parse and display without timestamp for stable output
                data = json.loads(line)
                data.pop("timestamp", None)  # Remove timestamp
                r.tln(f"  {json.dumps(data)}")

        # Verify test2 was removed
        lines = updated_content.strip().split("\n")
        r.tln(f"Number of cases after filtering: {len(lines)}")

        test_names = [json.loads(line)["name"] for line in lines if line.strip()]
        r.tln(f"Remaining test names: {test_names}")

        r.tln()
        if "test2" not in test_names and "test1" in test_names and "test3" in test_names:
            r.tln("✓ Removed test was successfully filtered out!")
        else:
            r.tln("✗ Test filtering did not work as expected")
            r.tln(f"Expected: ['test1', 'test3']")
            r.tln(f"Got: {test_names}")

    finally:
        # Clean up temporary directory
        shutil.rmtree(test_dir)

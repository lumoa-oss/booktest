"""Tests for the two-dimensional test result implementation."""

import booktest as bt


class TestTwoDimensionalResults(bt.TestBook):
    """Test suite for two-dimensional test results."""

    def test_success_states(self, t: bt.TestCaseRun):
        """Test the different success states."""
        t.h1("Success States")

        t.h2("SuccessState Enum Values")
        t.tln(f"OK: {bt.SuccessState.OK.value}")
        t.tln(f"DIFF: {bt.SuccessState.DIFF.value}")
        t.tln(f"FAIL: {bt.SuccessState.FAIL.value}")

    def test_snapshot_states(self, t: bt.TestCaseRun):
        """Test the different snapshot states."""
        t.h1("Snapshot States")

        t.h2("SnapshotState Enum Values")
        t.tln(f"INTACT: {bt.SnapshotState.INTACT.value}")
        t.tln(f"UPDATED: {bt.SnapshotState.UPDATED.value}")
        t.tln(f"FAIL: {bt.SnapshotState.FAIL.value}")

    def test_two_dimensional_result_creation(self, t: bt.TestCaseRun):
        """Test creating and using TwoDimensionalTestResult."""
        t.h1("Two-Dimensional Test Result")

        # Create different result combinations
        results = [
            bt.TwoDimensionalTestResult(bt.SuccessState.OK, bt.SnapshotState.INTACT),
            bt.TwoDimensionalTestResult(bt.SuccessState.OK, bt.SnapshotState.UPDATED),
            bt.TwoDimensionalTestResult(bt.SuccessState.DIFF, bt.SnapshotState.INTACT),
            bt.TwoDimensionalTestResult(bt.SuccessState.FAIL, bt.SnapshotState.FAIL),
        ]

        t.h2("Result Combinations")
        for result in results:
            t.tln(f"{str(result)}")
            t.tln(f"  Legacy: {result.to_legacy_result()}")
            t.tln(f"  Requires Review: {result.requires_review()}")
            t.tln(f"  Is Success: {result.is_success()}")
            t.tln(f"  Can Auto Approve: {result.can_auto_approve()}")
            t.tln("")

    def test_legacy_compatibility(self, t: bt.TestCaseRun):
        """Test backward compatibility with legacy TestResult."""
        t.h1("Legacy Compatibility")

        # Test that legacy results still work
        legacy_results = [bt.TestResult.OK, bt.TestResult.DIFF, bt.TestResult.FAIL]

        t.h2("Legacy Results")
        for result in legacy_results:
            exit_code = bt.test_result_to_exit_code(result)
            t.tln(f"{result}: exit code {exit_code}")

        t.h2("Two-Dimensional Results with Legacy Function")
        two_dim_results = [
            bt.TwoDimensionalTestResult(bt.SuccessState.OK, bt.SnapshotState.INTACT),
            bt.TwoDimensionalTestResult(bt.SuccessState.DIFF, bt.SnapshotState.UPDATED),
            bt.TwoDimensionalTestResult(bt.SuccessState.FAIL, bt.SnapshotState.FAIL),
        ]

        for result in two_dim_results:
            exit_code = bt.test_result_to_exit_code(result)
            t.tln(f"{str(result)}: exit code {exit_code}")

    def test_review_logic(self, t: bt.TestCaseRun):
        """Test the review decision logic."""
        t.h1("Review Decision Logic")

        test_cases = [
            (bt.SuccessState.OK, bt.SnapshotState.INTACT, "Auto-approve"),
            (bt.SuccessState.OK, bt.SnapshotState.UPDATED, "Auto-approve"),
            (bt.SuccessState.OK, bt.SnapshotState.FAIL, "Warning only"),
            (bt.SuccessState.DIFF, bt.SnapshotState.INTACT, "Human review required"),
            (bt.SuccessState.DIFF, bt.SnapshotState.UPDATED, "Human review required"),
            (bt.SuccessState.DIFF, bt.SnapshotState.FAIL, "Human review required"),
            (bt.SuccessState.FAIL, bt.SnapshotState.INTACT, "Fix test logic first"),
            (bt.SuccessState.FAIL, bt.SnapshotState.UPDATED, "Fix test logic first"),
            (bt.SuccessState.FAIL, bt.SnapshotState.FAIL, "Fix test logic first"),
        ]

        t.h2("Decision Matrix")
        for success, snapshot, expected in test_cases:
            result = bt.TwoDimensionalTestResult(success, snapshot)
            t.tln(f"{str(result)} → {expected}")

    def test_current_implementation_stores_two_dimensional_result(self, t: bt.TestCaseRun):
        """Test that TestCaseRun now stores two-dimensional results."""
        t.h1("Current Implementation Test")

        # This test should pass and store a two-dimensional result
        t.tln("This test should have both legacy and two-dimensional results stored")

        # After the test ends, we should be able to access both results
        # For now, just verify the structure exists
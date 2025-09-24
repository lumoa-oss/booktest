"""Demonstration of two-dimensional test results in action."""

import booktest as bt


class TestDemonstration(bt.TestBook):
    """Demonstrate the two-dimensional results system."""

    def test_passing_case(self, t: bt.TestCaseRun):
        """A test that should show OK/INTACT."""
        t.h1("Passing Test Case")
        t.tln("This test should pass and show OK/INTACT")
        t.tln("The two-dimensional result should be stored")

    def test_changing_case(self, t: bt.TestCaseRun):
        """A test that will show changes."""
        t.h1("Changing Test Case")
        t.tln("This test content might change")
        t.tln("Current timestamp-like value: 42")  # This can change to trigger DIFF

    def test_inspect_results(self, t: bt.TestCaseRun):
        """Inspect the internal result storage."""
        t.h1("Internal Result Inspection")

        # The two-dimensional result should be stored after end() is called
        # For now, just document the expectation
        t.tln("After this test ends, both legacy and two-dimensional results should be stored")
        t.tln("Legacy result accessible via: t.result")
        t.tln("Two-dimensional result accessible via: t.two_dimensional_result")
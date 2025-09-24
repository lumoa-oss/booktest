"""Test CLI display of two-dimensional results."""

import booktest as bt


class TestCLIDisplay(bt.TestBook):
    """Test different CLI display scenarios."""

    def test_ok_intact_result(self, t: bt.TestCaseRun):
        """Test that passes with intact snapshots."""
        t.h1("OK/INTACT Test")
        t.tln("This should show OK/INTACT in verbose mode")

    def test_simulated_diff_result(self, t: bt.TestCaseRun):
        """Test that will show DIFF when content changes."""
        t.h1("Content That May Change")
        t.tln("This is static content that should remain the same")
        t.tln("Static value: 200")  # Changed from 100 to 200

    def test_simulated_updated_result(self, t: bt.TestCaseRun):
        """Test demonstrating what UPDATED would look like."""
        t.h1("Simulated Updated Result")
        t.tln("In the future, this would show OK/UPDATED")
        t.tln("when snapshots are auto-refreshed")
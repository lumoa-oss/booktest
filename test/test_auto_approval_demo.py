"""Demonstration of auto-approval scenarios from ADR-002."""

import booktest as bt


class TestAutoApprovalDemo(bt.TestBook):
    """Demonstrate the key auto-approval scenarios."""

    def test_scenario_ok_intact(self, t: bt.TestCaseRun):
        """Scenario: Test passes, snapshots valid → OK/INTACT → No review needed."""
        t.h1("OK/INTACT Scenario")
        t.tln("✅ Test logic: PASSED")
        t.tln("✅ Snapshots: Valid and current")
        t.tln("→ Result: Can auto-approve, no human review needed")

    def test_scenario_ok_updated(self, t: bt.TestCaseRun):
        """Scenario: Test passes, snapshots refreshed → OK/UPDATED → No review needed."""
        t.h1("OK/UPDATED Scenario")
        t.tln("✅ Test logic: PASSED")
        t.tln("🔄 Snapshots: Auto-refreshed (external API changed)")
        t.tln("→ Result: Can auto-approve, no human review needed")
        t.tln("")
        t.tln("This is the key improvement from ADR-002:")
        t.tln("External dependency changes don't force human reviews!")

    def test_scenario_diff_intact(self, t: bt.TestCaseRun):
        """Scenario: Test logic changed → DIFF/INTACT → Human review required."""
        t.h1("DIFF/INTACT Scenario")
        t.tln("❓ Test logic: CHANGED (output differs)")
        t.tln("✅ Snapshots: Intact")
        t.tln("→ Result: Requires human review")
        t.tln("")
        t.tln("Human must verify the logic change is intentional")

    def test_scenario_fail_any(self, t: bt.TestCaseRun):
        """Scenario: Test fails → FAIL/* → Fix test logic first."""
        t.h1("FAIL/* Scenario")
        t.tln("❌ Test logic: FAILED (exception/assertion)")
        t.tln("? Snapshots: Irrelevant when test fails")
        t.tln("→ Result: Fix test logic first")
        t.tln("")
        t.tln("Snapshot state doesn't matter when test logic is broken")

    def test_decision_matrix(self, t: bt.TestCaseRun):
        """Show the complete decision matrix."""
        t.h1("Complete Decision Matrix")
        t.tln("")
        t.tln("| Success | Snapshot | Decision                    |")
        t.tln("|---------|----------|-----------------------------|")
        t.tln("| OK      | INTACT   | ✅ Auto-approve             |")
        t.tln("| OK      | UPDATED  | ✅ Auto-approve             |")
        t.tln("| OK      | FAIL     | ⚠️  Warning (snapshot error) |")
        t.tln("| DIFF    | INTACT   | ❓ Human review required     |")
        t.tln("| DIFF    | UPDATED  | ❓ Human review required     |")
        t.tln("| DIFF    | FAIL     | ❓ Human review required     |")
        t.tln("| FAIL    | *        | ❌ Fix test logic first     |")
        t.tln("")
        t.tln("The key insight: Only DIFF success states need human review")
        t.tln("Snapshot changes (UPDATED) can be handled automatically")
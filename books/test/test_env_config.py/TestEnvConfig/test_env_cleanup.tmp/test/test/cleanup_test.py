
import os
import booktest as bt

def test_check_env_vars(t: bt.TestCaseRun):
    """Verify env vars are set during test."""
    t.h1("Environment Variable Check")

    test_var = os.environ.get("TEST_CLEANUP_VAR", "NOT_SET")
    another_var = os.environ.get("ANOTHER_CLEANUP_VAR", "NOT_SET")

    t.tln(f"TEST_CLEANUP_VAR: {test_var}")
    t.tln(f"ANOTHER_CLEANUP_VAR: {another_var}")

    # Write values to file so parent test can verify they were set
    with open("env_values.txt", "w") as f:
        f.write(f"{test_var}\n{another_var}")

    assert test_var == "temporary_value", f"Expected 'temporary_value', got '{test_var}'"
    assert another_var == "another_temporary", f"Expected 'another_temporary', got '{another_var}'"

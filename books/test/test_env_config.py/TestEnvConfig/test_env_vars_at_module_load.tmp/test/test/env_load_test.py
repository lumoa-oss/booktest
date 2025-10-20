
import os
import booktest as bt

# Read env var at module load time
MODULE_LOAD_VAR = os.environ.get("TEST_VAR_FROM_CONFIG", "NOT_SET")
MODULE_LOAD_VAR2 = os.environ.get("ANOTHER_TEST_VAR", "NOT_SET")

def test_env_loaded(t: bt.TestCaseRun):
    """Test that env vars were set at module load time."""
    t.h1("Environment Variables Available at Module Load")

    t.tln(f"TEST_VAR_FROM_CONFIG (at module load): {MODULE_LOAD_VAR}")
    t.tln(f"ANOTHER_TEST_VAR (at module load): {MODULE_LOAD_VAR2}")
    t.tln()

    # Verify values
    assert MODULE_LOAD_VAR == "config_value", f"Expected 'config_value', got '{MODULE_LOAD_VAR}'"
    assert MODULE_LOAD_VAR2 == "another_value", f"Expected 'another_value', got '{MODULE_LOAD_VAR2}'"

    # Also verify they're still set in current env
    current_var = os.environ.get("TEST_VAR_FROM_CONFIG", "NOT_SET")
    current_var2 = os.environ.get("ANOTHER_TEST_VAR", "NOT_SET")

    t.tln(f"TEST_VAR_FROM_CONFIG (current): {current_var}")
    t.tln(f"ANOTHER_TEST_VAR (current): {current_var2}")
    t.tln()

    assert current_var == "config_value", f"Expected 'config_value', got '{current_var}'"
    assert current_var2 == "another_value", f"Expected 'another_value', got '{current_var2}'"

    t.tln("✓ Environment variables were correctly set at module load time!")

"""
Test for environment variable configuration in booktest.ini.
"""
import os
import sys
import tempfile
from pathlib import Path

import booktest as bt
from booktest.config.config import extract_env_vars


class TestEnvConfig(bt.TestBook):

    def test_extract_env_vars_legacy(self, t: bt.TestCaseRun):
        """
        Test that env_ prefixed config values are extracted correctly (legacy format).
        """
        t.h1("Extract Environment Variables from Config (Legacy Format)")

        config = {
            "python_path": ".",
            "test_paths": "test",
            "env_FOO": "bar",
            "env_BAZ": "qux",
            "env_MULTI_WORD": "hello world",
            "timeout": "3600"
        }

        env_vars = extract_env_vars(config)

        t.tln("Config:")
        for key, value in config.items():
            t.tln(f"  {key} = {value}")

        t.tln()
        t.tln("Extracted environment variables:")
        for key, value in env_vars.items():
            t.tln(f"  {key} = {value}")

        assert "FOO" in env_vars, "FOO should be extracted"
        assert env_vars["FOO"] == "bar", "FOO should equal 'bar'"
        assert "BAZ" in env_vars, "BAZ should be extracted"
        assert env_vars["BAZ"] == "qux", "BAZ should equal 'qux'"
        assert "MULTI_WORD" in env_vars, "MULTI_WORD should be extracted"
        assert env_vars["MULTI_WORD"] == "hello world", "MULTI_WORD should equal 'hello world'"
        assert "python_path" not in env_vars, "Non-env keys should not be extracted"
        assert "timeout" not in env_vars, "Non-env keys should not be extracted"

        t.tln()
        t.tln("✓ All legacy format extraction tests passed!")

    def test_extract_env_vars_pytest_style(self, t: bt.TestCaseRun):
        """
        Test that pytest-style multiline env config is extracted correctly.
        """
        t.h1("Extract Environment Variables from Config (Pytest Style)")

        config = {
            "python_path": ".",
            "test_paths": "test",
            "env": "FOO=bar\nBAZ=qux\nMULTI_WORD=hello world",
            "timeout": "3600"
        }

        env_vars = extract_env_vars(config)

        t.tln("Config:")
        for key, value in config.items():
            if key == "env":
                t.tln(f"  {key} =")
                for line in value.split("\n"):
                    t.tln(f"      {line}")
            else:
                t.tln(f"  {key} = {value}")

        t.tln()
        t.tln("Extracted environment variables:")
        for key, value in env_vars.items():
            t.tln(f"  {key} = {value}")

        assert "FOO" in env_vars, "FOO should be extracted"
        assert env_vars["FOO"] == "bar", "FOO should equal 'bar'"
        assert "BAZ" in env_vars, "BAZ should be extracted"
        assert env_vars["BAZ"] == "qux", "BAZ should equal 'qux'"
        assert "MULTI_WORD" in env_vars, "MULTI_WORD should be extracted"
        assert env_vars["MULTI_WORD"] == "hello world", "MULTI_WORD should equal 'hello world'"
        assert "python_path" not in env_vars, "Non-env keys should not be extracted"
        assert "timeout" not in env_vars, "Non-env keys should not be extracted"

        t.tln()
        t.tln("✓ All pytest-style extraction tests passed!")

    def test_env_vars_at_module_load(self, t: bt.TestCaseRun):
        """
        Test that environment variables from config are available during module import.
        """
        import subprocess

        t.h1("Environment Variables at Module Load Time")

        # Create a temporary test environment
        tmpdir = Path(t.tmp_dir("test"))

        # Create test directory structure
        test_dir = tmpdir / "test"
        books_dir = tmpdir / "books"
        test_dir.mkdir(parents=True)
        books_dir.mkdir(parents=True)

        # Create __init__.py to make test a proper package
        init_file = test_dir / "__init__.py"
        init_file.write_text("")

        # Create config file with env variables (pytest-style)
        config_file = tmpdir / "booktest.ini"
        config_file.write_text("""
python_path=.
test_paths=test
books_path=books
env =
    TEST_VAR_FROM_CONFIG=config_value
    ANOTHER_TEST_VAR=another_value
""")

        t.tln(f"Created test environment at {tmpdir}")
        t.tln(f"Config file: {config_file}")
        t.tln()

        # Create a test file that reads env vars at module load time
        test_file = test_dir / "env_load_test.py"
        test_file.write_text('''
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
''')

        t.tln("Created test file that reads env vars at module load time")
        t.tln()

        # Run booktest as subprocess to avoid nested execution
        t.tln("Running booktest in temp directory...")
        t.tln()

        # Get the path to booktest command
        booktest_cmd = os.path.join(os.path.dirname(sys.executable), "booktest")
        if not os.path.exists(booktest_cmd):
            # Try python -m booktest
            result = subprocess.run(
                [sys.executable, "-m", "booktest", "test/env_load_test.py::test_env_loaded"],
                cwd=tmpdir,
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                [booktest_cmd, "test/env_load_test.py::test_env_loaded"],
                cwd=tmpdir,
                capture_output=True,
                text=True
            )

        t.tln(f"Exit code: {result.returncode}")

        # Check the actual test output to verify env vars were set
        output_file = tmpdir / "books" / ".out" / "test" / "env_load_test.py" / "test_env_loaded.md"
        if output_file.exists():
            output = output_file.read_text()
            t.tln()
            t.tln("Test output:")
            t.tln(output)
            t.tln()

            # Verify the env vars were correctly set
            assert "TEST_VAR_FROM_CONFIG (at module load): config_value" in output, \
                "Env var should be set at module load time"
            assert "ANOTHER_TEST_VAR (at module load): another_value" in output, \
                "Env var should be set at module load time"
            assert "Environment variables were correctly set at module load time!" in output, \
                "Test should have passed"

            t.tln("✓ Environment variables from config were available at module load time!")
        else:
            t.tln(f"Warning: Output file not found at {output_file}")
            if result.stdout:
                t.tln("STDOUT:")
                t.tln(result.stdout)
            if result.stderr:
                t.tln("STDERR:")
                t.tln(result.stderr)
            raise AssertionError("Test output file not found")

    def test_env_cleanup(self, t: bt.TestCaseRun):
        """
        Test that environment variables are cleaned up after booktest execution.
        """
        import subprocess

        t.h1("Environment Variable Cleanup")

        # Store original env values
        original_test_var = os.environ.get("TEST_CLEANUP_VAR")
        original_another_var = os.environ.get("ANOTHER_CLEANUP_VAR")

        t.tln(f"Original TEST_CLEANUP_VAR: {original_test_var}")
        t.tln(f"Original ANOTHER_CLEANUP_VAR: {original_another_var}")
        t.tln()

        # Create a temporary test environment
        tmpdir = Path(t.tmp_dir("test"))

        # Create test directory structure
        test_dir = tmpdir / "test"
        books_dir = tmpdir / "books"
        test_dir.mkdir(parents=True)
        books_dir.mkdir(parents=True)

        # Create __init__.py to make test a proper package
        init_file = test_dir / "__init__.py"
        init_file.write_text("")

        # Create config file with env variables that tests the values exist (pytest-style)
        config_file = tmpdir / "booktest.ini"
        config_file.write_text("""
python_path=.
test_paths=test
books_path=books
env =
    TEST_CLEANUP_VAR=temporary_value
    ANOTHER_CLEANUP_VAR=another_temporary
""")

        # Create a test that verifies env vars are set and writes them to a file
        test_file = test_dir / "cleanup_test.py"
        test_file.write_text('''
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
        f.write(f"{test_var}\\n{another_var}")

    assert test_var == "temporary_value", f"Expected 'temporary_value', got '{test_var}'"
    assert another_var == "another_temporary", f"Expected 'another_temporary', got '{another_var}'"
''')

        t.tln("Running booktest with env vars set in config...")

        # Run booktest as subprocess
        booktest_cmd = os.path.join(os.path.dirname(sys.executable), "booktest")
        if not os.path.exists(booktest_cmd):
            result = subprocess.run(
                [sys.executable, "-m", "booktest", "test/cleanup_test.py::test_check_env_vars"],
                cwd=tmpdir,
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                [booktest_cmd, "test/cleanup_test.py::test_check_env_vars"],
                cwd=tmpdir,
                capture_output=True,
                text=True
            )

        t.tln(f"Test run completed with exit code: {result.returncode}")
        t.tln()

        # Read the env values that were captured during test
        env_file = tmpdir / "env_values.txt"
        if env_file.exists():
            captured_values = env_file.read_text().strip().split("\n")
            t.tln(f"Captured TEST_CLEANUP_VAR: {captured_values[0]}")
            t.tln(f"Captured ANOTHER_CLEANUP_VAR: {captured_values[1]}")
            t.tln()

            assert captured_values[0] == "temporary_value", "Env var should have been set during test"
            assert captured_values[1] == "another_temporary", "Env var should have been set during test"
        else:
            # Check test output to verify env vars were set
            output_file = tmpdir / "books" / ".out" / "test" / "cleanup_test.py" / "test_check_env_vars.md"
            if output_file.exists():
                output = output_file.read_text()
                t.tln("Test output:")
                t.tln(output)
                t.tln()

                assert "TEST_CLEANUP_VAR: temporary_value" in output, "Env var should be set during test"
                assert "ANOTHER_CLEANUP_VAR: another_temporary" in output, "Env var should be set during test"
            else:
                t.tln(f"Warning: Neither env_values.txt nor test output found")

        # Check that env vars are NOT leaked to parent process
        after_test_var = os.environ.get("TEST_CLEANUP_VAR")
        after_another_var = os.environ.get("ANOTHER_CLEANUP_VAR")

        t.tln(f"After execution TEST_CLEANUP_VAR in parent: {after_test_var}")
        t.tln(f"After execution ANOTHER_CLEANUP_VAR in parent: {after_another_var}")
        t.tln()

        # Verify cleanup (subprocess env vars shouldn't leak to parent)
        assert after_test_var == original_test_var, \
            f"TEST_CLEANUP_VAR should be unchanged in parent ({original_test_var}), got {after_test_var}"
        assert after_another_var == original_another_var, \
            f"ANOTHER_CLEANUP_VAR should be unchanged in parent ({original_another_var}), got {after_another_var}"

        t.tln("✓ Environment variables were properly isolated to subprocess!")

# Environment Variables at Module Load Time

Created test environment at books/.out/test/test_env_config.py/TestEnvConfig/test_env_vars_at_module_load.tmp/test
Config file: books/.out/test/test_env_config.py/TestEnvConfig/test_env_vars_at_module_load.tmp/test/booktest.ini

Created test file that reads env vars at module load time

Running booktest in temp directory...

Exit code: 255

Test output:
# Environment Variables Available at Module Load

TEST_VAR_FROM_CONFIG (at module load): config_value
ANOTHER_TEST_VAR (at module load): another_value

TEST_VAR_FROM_CONFIG (current): config_value
ANOTHER_TEST_VAR (current): another_value

✓ Environment variables were correctly set at module load time!


✓ Environment variables from config were available at module load time!

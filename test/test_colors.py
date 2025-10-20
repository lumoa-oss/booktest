"""
Test for color output functionality.
"""
import os
import booktest as bt
from booktest.reporting import colors


class TestColors(bt.TestBook):

    def test_color_functions(self, t: bt.TestCaseRun):
        """
        Test that color functions work correctly.
        """
        t.h1("Color Functions Test")

        # Test with colors disabled
        colors.set_color_enabled(False)

        t.h2("Colors Disabled")
        t.tln(f"is_color_enabled: {colors.is_color_enabled()}")
        t.tln(f"red('ERROR'): {colors.red('ERROR')!r}")
        t.tln(f"yellow('WARNING'): {colors.yellow('WARNING')!r}")
        t.tln()

        assert colors.red('ERROR') == 'ERROR', "Colors should be plain text when disabled"
        assert colors.yellow('WARNING') == 'WARNING', "Colors should be plain text when disabled"

        # Test with colors enabled
        colors.set_color_enabled(True)

        t.h2("Colors Enabled")
        t.tln(f"is_color_enabled: {colors.is_color_enabled()}")
        t.tln(f"red('ERROR'): {colors.red('ERROR')!r}")
        t.tln(f"yellow('WARNING'): {colors.yellow('WARNING')!r}")
        t.tln()

        # Check that ANSI codes are present when enabled
        red_text = colors.red('ERROR')
        yellow_text = colors.yellow('WARNING')

        assert '\033[' in red_text, "Red text should contain ANSI codes"
        assert '\033[' in yellow_text, "Yellow text should contain ANSI codes"
        assert 'ERROR' in red_text, "Red text should contain the original text"
        assert 'WARNING' in yellow_text, "Yellow text should contain the original text"

        t.tln("✓ All color function tests passed!")

    def test_no_color_env_var(self, t: bt.TestCaseRun):
        """
        Test that NO_COLOR environment variable disables colors.
        """
        t.h1("NO_COLOR Environment Variable Test")

        # Save original state
        original_no_color = os.environ.get('NO_COLOR')

        try:
            # Test without NO_COLOR - enable colors explicitly for testing
            if 'NO_COLOR' in os.environ:
                del os.environ['NO_COLOR']

            # Force re-check and explicitly enable colors (CI might not have TTY)
            import importlib
            importlib.reload(colors)
            colors.set_color_enabled(True)  # Force enable for testing

            t.tln(f"Without NO_COLOR: is_color_enabled = {colors.is_color_enabled()}")

            # Test with NO_COLOR set
            os.environ['NO_COLOR'] = '1'
            importlib.reload(colors)

            t.tln(f"With NO_COLOR: is_color_enabled = {colors.is_color_enabled()}")
            t.tln()

            assert not colors.is_color_enabled(), "Colors should be disabled when NO_COLOR is set"
            assert colors.red('ERROR') == 'ERROR', "Output should be plain text with NO_COLOR"

            t.tln("✓ NO_COLOR environment variable respected!")

        finally:
            # Restore original state
            if original_no_color is not None:
                os.environ['NO_COLOR'] = original_no_color
            elif 'NO_COLOR' in os.environ:
                del os.environ['NO_COLOR']

            # Reload to restore original state
            import importlib
            importlib.reload(colors)

    def test_colorize_utility(self, t: bt.TestCaseRun):
        """
        Test the colorize utility function.
        """
        t.h1("Colorize Utility Test")

        colors.set_color_enabled(True)

        t.tln("Testing different colors:")
        t.tln(f"  red:    {colors.red('This is red')!r}")
        t.tln(f"  yellow: {colors.yellow('This is yellow')!r}")
        t.tln(f"  green:  {colors.green('This is green')!r}")
        t.tln(f"  blue:   {colors.blue('This is blue')!r}")
        t.tln(f"  gray:   {colors.gray('This is gray')!r}")
        t.tln()

        # Verify all color functions return colored text
        assert '\033[91m' in colors.red('test'), "Red should use color code 91"
        assert '\033[93m' in colors.yellow('test'), "Yellow should use color code 93"
        assert '\033[92m' in colors.green('test'), "Green should use color code 92"
        assert '\033[94m' in colors.blue('test'), "Blue should use color code 94"
        assert '\033[90m' in colors.gray('test'), "Gray should use color code 90"

        t.tln("✓ All colors verified!")

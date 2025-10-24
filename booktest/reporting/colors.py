"""
ANSI color code utilities for terminal output.
"""
import os
import sys


# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    RED = '\033[91m'      # Bright red for errors
    YELLOW = '\033[93m'   # Bright yellow for diffs
    GREEN = '\033[92m'    # Bright green
    BLUE = '\033[94m'     # Bright blue
    CYAN = '\033[96m'     # Bright cyan for info
    GRAY = '\033[90m'     # Gray (bright black)
    BRIGHT_WHITE = '\033[97m'    # Bright white
    DIM = '\033[2m'       # Dim/faint
    BOLD = '\033[1m'      # Bold


def _supports_color():
    """
    Check if the terminal supports color output.

    Returns False if:
    - NO_COLOR environment variable is set (https://no-color.org/)
    - Not running in a TTY
    - Running on Windows without ANSICON/WT_SESSION
    """
    # Respect NO_COLOR environment variable
    if os.environ.get('NO_COLOR'):
        return False

    # Check if output is a TTY
    if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
        return False

    # Windows terminal support
    if sys.platform == 'win32':
        # Windows Terminal and modern Windows 10+ support ANSI
        if os.environ.get('WT_SESSION') or os.environ.get('ANSICON'):
            return True
        # Try to enable ANSI on Windows 10+
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False

    return True


# Global color support check
_COLOR_ENABLED = _supports_color()


def colorize(text: str, color: str) -> str:
    """
    Wrap text with ANSI color codes if color is enabled.

    Args:
        text: Text to colorize
        color: ANSI color code from Colors class

    Returns:
        Colorized text if colors are enabled, otherwise plain text
    """
    if not _COLOR_ENABLED:
        return text
    return f"{color}{text}{Colors.RESET}"


def red(text: str) -> str:
    """Colorize text in red (for errors)."""
    return colorize(text, Colors.RED)


def yellow(text: str) -> str:
    """Colorize text in yellow (for diffs)."""
    return colorize(text, Colors.YELLOW)


def green(text: str) -> str:
    """Colorize text in green."""
    return colorize(text, Colors.GREEN)


def blue(text: str) -> str:
    """Colorize text in blue."""
    return colorize(text, Colors.BLUE)


def gray(text: str) -> str:
    """Colorize text in gray."""
    return colorize(text, Colors.GRAY)


def cyan(text: str) -> str:
    """Colorize text in cyan."""
    return colorize(text, Colors.CYAN)


def white(text: str) -> str:
    """Colorize text in bright white."""
    return colorize(text, Colors.BRIGHT_WHITE)


def dim_gray(text: str) -> str:
    """Colorize text in dim gray (more subtle than regular gray)."""
    if not _COLOR_ENABLED:
        return text
    return f"{Colors.DIM}{Colors.GRAY}{text}{Colors.RESET}"


def default_color(text: str) -> str:
    """Return text in terminal's default color (adapts to light/dark themes)."""
    if not _COLOR_ENABLED:
        return text
    return f"{Colors.RESET}{text}{Colors.RESET}"


def is_color_enabled() -> bool:
    """Check if color output is enabled."""
    return _COLOR_ENABLED


def set_color_enabled(enabled: bool):
    """
    Override color support detection.

    Args:
        enabled: True to enable colors, False to disable
    """
    global _COLOR_ENABLED
    _COLOR_ENABLED = enabled

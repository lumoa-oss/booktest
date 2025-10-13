"""
Base output interface for test case writing and review.

This module provides a common interface for writing output in both
regular test cases (TestCaseRun) and GPT-assisted reviews (GptReview).
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class OutputWriter(ABC):
    """
    Abstract base class for output writing.

    Provides common methods for writing markdown-formatted output including:
    - Headers (h1, h2, h3)
    - Text output (tln, iln)
    - Inline text (i, key)
    - Tables and dataframes (ttable, tdf)
    - Code blocks (tcode, icode)
    - Anchors for non-linear comparison
    """

    @abstractmethod
    def h(self, level: int, title: str):
        """Write a header at the specified level."""
        pass

    def h1(self, title: str):
        """Write a level 1 header."""
        self.h(1, title)

    def h2(self, title: str):
        """Write a level 2 header."""
        self.h(2, title)

    def h3(self, title: str):
        """Write a level 3 header."""
        self.h(3, title)

    @abstractmethod
    def i(self, text: str):
        """Write inline text (info - not compared against snapshots)."""
        pass

    @abstractmethod
    def iln(self, text: str = ""):
        """Write a line of info text (not compared against snapshots)."""
        pass

    @abstractmethod
    def tln(self, text: str = ""):
        """Write a line of tested text (compared against snapshots)."""
        pass

    @abstractmethod
    def key(self, key: str):
        """Write a key for key-value output."""
        pass

    @abstractmethod
    def anchor(self, anchor: str):
        """
        Create an anchor point for non-linear snapshot comparison.

        Anchors allow the test to find matching points in the snapshot
        even when content order or line counts vary.
        """
        pass

    @abstractmethod
    def ttable(self, table: dict):
        """Write a table from a dictionary."""
        pass

    @abstractmethod
    def tdf(self, df: Any):
        """Write a pandas dataframe as a table."""
        pass

    def tcode(self, code: str, lang: str = ""):
        """
        Write a code block (tested).

        Args:
            code: The code content
            lang: Optional language identifier for syntax highlighting
        """
        if lang:
            self.tln(f"```{lang}")
        else:
            self.tln("```")
        self.tln(code)
        self.tln("```")

    def icode(self, code: str, lang: str = ""):
        """
        Write a code block (info - not tested).

        Args:
            code: The code content
            lang: Optional language identifier for syntax highlighting
        """
        if lang:
            self.iln(f"```{lang}")
        else:
            self.iln("```")
        self.iln(code)
        self.iln("```")

    def icodeln(self, code: str, lang: str = ""):
        """Alias for icode for backwards compatibility."""
        self.icode(code, lang)

    def tcodeln(self, code: str, lang: str = ""):
        """Alias for tcode."""
        self.tcode(code, lang)

"""
Base output interface for test case writing and review.

This module provides a common interface for writing output in both
regular test cases (TestCaseRun) and GPT-assisted reviews (GptReview).

The architecture uses a small set of primitive abstract methods (t, i, fail, h)
and builds all other methods on top of these primitives.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class OutputWriter(ABC):
    """
    Abstract base class for output writing.

    Provides common methods for writing markdown-formatted output including:
    - Headers (h1, h2, h3) - built on h()
    - Text output (tln, iln, key, anchor, assertln) - built on t(), i(), fail()
    - Tables and dataframes (ttable, tdf) - built on t(), i()
    - Code blocks (tcode, icode) - built on tln(), iln()

    Subclasses must implement:
    - h(level, title): Write a header
    - t(text): Write tested text inline
    - i(text): Write info text inline
    - fail(): Mark current line as failed
    """

    # ========== Abstract primitive methods ==========

    @abstractmethod
    def h(self, level: int, title: str):
        """
        Write a header at the specified level.

        This is a primitive method that must be implemented by subclasses.
        TestCaseRun uses header() which includes anchoring logic.
        GptReview writes directly to buffer and delegates to TestCaseRun.
        """
        pass

    @abstractmethod
    def t(self, text: str):
        """
        Write tested text inline (no newline).

        This is a primitive method that must be implemented by subclasses.
        In TestCaseRun, this is compared against snapshots.
        In GptReview, this is added to buffer and delegated to TestCaseRun.
        """
        pass

    @abstractmethod
    def i(self, text: str):
        """
        Write info text inline (no newline, not compared against snapshots).

        This is a primitive method that must be implemented by subclasses.
        In TestCaseRun, this bypasses snapshot comparison.
        In GptReview, this is added to buffer and delegated to TestCaseRun.
        """
        pass

    @abstractmethod
    def fail(self):
        """
        Mark the current line as failed.

        This is a primitive method that must be implemented by subclasses.
        Returns self for method chaining.
        """
        pass

    # ========== Concrete methods built on primitives ==========

    def h1(self, title: str):
        """Write a level 1 header."""
        self.h(1, title)
        return self

    def h2(self, title: str):
        """Write a level 2 header."""
        self.h(2, title)
        return self

    def h3(self, title: str):
        """Write a level 3 header."""
        self.h(3, title)
        return self

    def h4(self, title: str):
        """Write a level 4 header."""
        self.h(4, title)
        return self

    def h5(self, title: str):
        """Write a level 4 header."""
        self.h(5, title)
        return self

    def tln(self, text: str = ""):
        """
        Write a line of tested text (compared against snapshots).
        Built on t() primitive.
        """
        self.t(text)
        self.t("\n")
        return self

    def iln(self, text: str = ""):
        """
        Write a line of info text (not compared against snapshots).
        Built on i() primitive.
        """
        self.i(text)
        self.i("\n")
        return self

    def key(self, key: str):
        """
        Write a key prefix for key-value output.
        Built on t() and i() primitives.

        Note: TestCaseRun overrides this to add anchor() functionality.
        """
        self.t(key)
        self.i(" ")
        return self

    def anchor(self, anchor: str):
        """
        Create an anchor point for non-linear snapshot comparison.
        Default implementation just writes the anchor text.

        Note: TestCaseRun overrides this to add seek_prefix() functionality.
        """
        self.t(anchor)
        return self

    def assertln(self, cond: bool, error_message: Optional[str] = None):
        """
        Assert a condition and print ok/FAILED.
        Built on i(), fail() primitives.
        """
        if cond:
            self.iln("ok")
        else:
            self.fail()
            if error_message:
                self.iln(error_message)
            else:
                self.iln("FAILED")
        return self

    def ttable(self, table: dict):
        """
        Write a markdown table from a dictionary of columns.
        Built on tdf() which is built on t() and i() primitives.

        Example:
            t.ttable({"x": [1, 2, 3], "y": [2, 3, 4]})
        """
        import pandas as pd
        return self.tdf(pd.DataFrame(table))

    def tdf(self, df: Any):
        """
        Write a pandas dataframe as a markdown table.
        Built on t() and i() primitives.

        Args:
            df: pandas DataFrame or compatible object with .columns and .index
        """
        # Calculate column widths
        pads = []
        for column in df.columns:
            max_len = len(column)
            for i in df.index:
                max_len = max(max_len, len(str(df[column][i])))
            pads.append(max_len)

        # Write header row
        buf = "|"
        for i, column in enumerate(df.columns):
            buf += column.ljust(pads[i])
            buf += "|"
        self.iln(buf)

        # Write separator row
        buf = "|"
        for i in pads:
            buf += "-" * i
            buf += "|"
        self.tln(buf)

        # Write data rows
        for i in df.index:
            self.t("|")
            for j, column in enumerate(df.columns):
                buf = str(df[column][i])\
                          .replace("\r", " ")\
                          .replace("\n", " ")\
                          .strip()

                self.t(buf)
                self.i(" " * (pads[j]-len(buf)))
                self.t("|")
            self.tln()

        return self

    def tcode(self, code: str, lang: str = ""):
        """
        Write a code block (tested).
        Built on tln() primitive.

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
        return self

    def icode(self, code: str, lang: str = ""):
        """
        Write a code block (info - not tested).
        Built on iln() primitive.

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
        return self

    def icodeln(self, code: str, lang: str = ""):
        """Alias for icode for backwards compatibility."""
        return self.icode(code, lang)

    def tcodeln(self, code: str, lang: str = ""):
        """Alias for tcode."""
        return self.tcode(code, lang)

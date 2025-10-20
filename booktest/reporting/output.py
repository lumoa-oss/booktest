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
    def diff(self):
        """
        Flags the current line as different for review purposes.

        This is a primitive method that must be implemented by subclasses.
        Returns self for method chaining.
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

    def tmetric(self, value: float, tolerance: float, unit: str = None, direction: str = None):
        """
        Test a metric value with tolerance for acceptable variation.

        Compares current metric against snapshot value and accepts changes within
        tolerance. Useful for ML metrics that naturally fluctuate (accuracy, F1, etc).

        Args:
            value: Current metric value
            tolerance: Acceptable absolute difference from baseline
            unit: Optional unit for display (e.g., "%", "ms", "sec")
            direction: Optional constraint:
                - ">=" : Only fail on drops (value < baseline - tolerance)
                - "<=" : Only fail on increases (value > baseline + tolerance)
                - None : Fail if abs(value - baseline) > tolerance

        Behavior:
            - If no snapshot exists: Record as baseline
            - If within tolerance: Show delta but mark OK
            - If exceeds tolerance: Mark as FAIL (using fail() primitive)

        Example:
            t.tmetric(0.973, tolerance=0.02)  # Accuracy ±2%
            t.tmetric(97.3, tolerance=2, unit="%")  # Same, with units
            t.tmetric(0.973, tolerance=0.02, direction=">=")  # Only fail on drops
            t.tmetric(latency_ms, tolerance=5, unit="ms", direction="<=")  # No increases

        Output examples:
            0.973 (baseline)                           # First run
            0.973 (was 0.950, Δ+0.023)                # DIFF within tolerance → OK
            0.920 (was 0.950, Δ-0.030)                # Exceeds tolerance → FAIL
            97.3% (was 95.0%, Δ+2.3%)                 # With units
        """
        # Get expected value from snapshot
        old = self._get_expected_token()
        try:
            old_value = float(old) if old is not None else None
        except ValueError:
            old_value = None

        unit_str = unit if unit else ""

        if old_value is None:
            # No baseline - establish one
            if unit_str:
                self.tln(f"{value:.3f}{unit_str} (baseline)")
            else:
                self.tln(f"{value:.3f} (baseline)")
        else:
            delta = value - old_value

            # Check if within tolerance
            exceeds_tolerance = abs(delta) > tolerance

            # Check direction constraint
            violates_direction = False
            if direction == ">=" and delta < -tolerance:
                violates_direction = True
            elif direction == "<=" and delta > tolerance:
                violates_direction = True

            # Format delta string with appropriate sign
            if delta >= 0:
                delta_str = f"+{delta:.3f}"
            else:
                delta_str = f"{delta:.3f}"

            # Mark as failed if tolerance or direction violated
            if exceeds_tolerance or violates_direction:
                delta_str += f"<{tolerance:.3f}!"
                self.diff()

            # Write output with delta
            if unit_str:
                self.iln(f"{value:.3f}{unit_str} (was {old_value:.3f}{unit_str}, Δ{delta_str}{unit_str})")
            else:
                self.iln(f"{value:.3f} (was {old_value:.3f}, Δ{delta_str})")

        return self

    def tmetric_pct(self, value: float, tolerance_pct: float, unit: str = None, direction: str = None):
        """
        Test metric with percentage-based tolerance.

        Instead of absolute tolerance, uses percentage of baseline value.
        For example, tolerance_pct=5 means accept ±5% change from baseline.

        Args:
            value: Current value
            tolerance_pct: Acceptable percentage change (e.g., 5 for ±5%)
            unit: Optional display unit
            direction: Optional constraint ">=" or "<="

        Example:
            # 100 → 95: 5% drop → within 5% → OK
            # 100 → 90: 10% drop → exceeds 5% → FAIL
            t.tmetric_pct(95, tolerance_pct=5, unit="ms")
        """
        # Get expected value from snapshot
        old = self._get_expected_token()
        try:
            old_value = float(old) if old is not None else None
        except ValueError:
            old_value = None

        unit_str = unit if unit else ""

        if old_value is None:
            # No baseline - establish one
            if unit_str:
                self.tln(f"{value:.3f}{unit_str} (baseline)")
            else:
                self.tln(f"{value:.3f} (baseline)")
        else:
            delta = value - old_value
            delta_pct = (delta / old_value * 100) if old_value != 0 else 0

            # Calculate absolute tolerance from percentage
            tolerance = abs(old_value * tolerance_pct / 100)

            # Check if within tolerance
            exceeds_tolerance = abs(delta) > tolerance

            # Check direction constraint
            violates_direction = False
            if direction == ">=" and delta < -tolerance:
                violates_direction = True
            elif direction == "<=" and delta > tolerance:
                violates_direction = True

            # Format delta string with appropriate sign
            if delta >= 0:
                delta_str = f"+{delta:.3f}"
                delta_pct_str = f"+{delta_pct:.1f}%"
            else:
                delta_str = f"{delta:.3f}"
                delta_pct_str = f"{delta_pct:.1f}%"

            # Mark as failed if tolerance or direction violated
            if exceeds_tolerance or violates_direction:
                delta_str += f"<{tolerance:.3f}!"
                self.diff()

            # Write output with delta and percentage
            if unit_str:
                self.iln(f"{value:.3f}{unit_str} (was {old_value:.3f}{unit_str}, Δ{delta_str}{unit_str} [{delta_pct_str}])")
            else:
                self.iln(f"{value:.3f} (was {old_value:.3f}, Δ{delta_str} [{delta_pct_str}])")

        return self

    def _get_expected_token(self):
        """
        Get the next expected token from snapshot without advancing cursor.

        This is a helper method for metric tracking. Subclasses should override
        if they have snapshot comparison capability. Default returns None.
        """
        # Default implementation - subclasses override
        # TestCaseRun overrides with head_exp_token()
        return None

"""
Base output interface for test case writing and review.

This module provides a common interface for writing output in both
regular test cases (TestCaseRun) and GPT-assisted reviews (GptReview).

The architecture uses a small set of primitive abstract methods (t, i, fail, h)
and builds all other methods on top of these primitives.
"""
import json
import sys
import time
from abc import ABC, abstractmethod
from typing import Any, Optional
import os


class OutputWriter(ABC):
    """
    Abstract base class for output writing.

    Provides common methods for writing markdown-formatted output including:
    - Headers (h1, h2, h3) - built on h()
    - Text output (tln, iln, key, anchor, assertln) - built on t(), i(), fail()
    - Tables and dataframes (ttable, tdf, itable, idf) - built on t(), i() via _table()
    - Code blocks (tcode, icode) - built on tln(), iln()
    - Images (timage, iimage) - implemented in TestCaseRun

    Subclasses must implement:
    - h(level, title): Write a header
    - t(text): Write tested text inline (compared against snapshots)
    - i(text): Write info text inline (not tested, but shown in diffs)
    - fail(): Mark current line as failed
    - diff(): Mark current line as different
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
        In TestCaseRun, this bypasses snapshot comparison but still shows
        differences in 'new | old' format for AI review context.
        In GptReview, this is added to buffer and delegated to TestCaseRun.
        """
        pass

    @abstractmethod
    def f(self, text: str):
        """
        Write failed text inline (no newline), marking it as failed.

        This is a primitive method that must be implemented by subclasses.
        In TestCaseRun, this feeds text and marks each token as failed (red).
        In GptReview, this is added to buffer and delegated to TestCaseRun.
        """
        pass

    @abstractmethod
    def info_token(self):
        """
        Flags the previous token as different in non-breaking way for review purposes.

        This is a primitive method that must be implemented by subclasses.
        Returns self for method chaining.
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
    def diff_token(self):
        """
        Flags the previous token as different for review purposes.

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


    @abstractmethod
    def fail_token(self):
        """
        Mark the previous token as failed.

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

        Info output appears in test results and is written to both old and new
        output files. When content changes, it shows in 'new | old' format for
        AI review without marking the test as failed.
        """
        self.i(text)
        self.i("\n")
        return self

    def failln(self, text: str = ""):
        """
        Write a line of failed text, marking the entire line as failed (red).
        Built on f() and fail() primitives.

        All text in the line will be colored red in the output. The line will
        be marked as failed, causing the test to fail.
        """
        self.f(text)
        self.fail()
        self.f("\n")
        return self

    def fln(self, text: str = ""):
        """
        Write failed tokens based on f() primitive
        """
        self.f(text)
        self.f("\n")
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

    def keyvalueln(self, key: str, value: str):
        """
        Write a key-value pair on a single line.
        Built on key() and tln() primitives.

        Example:
            t.keyvalueln("Name:", "Alice")  # Output: "Name: Alice"
        """
        return self.key(key).tln(value)

    def header(self, header):
        """
        creates a header line that also operates as an anchor.

        the only difference between this method and anchorln() method is that the
        header is preceded and followed by an empty line.
        """
        if self.line_number > 0:
            check = self.last_checked and self.exp_line is not None
            self.feed_token("\n", check=check)
        self.anchorln(header)
        self.iln("")
        return self


    def tmsln(self, f, max_ms):
        """
        runs the function f and measures the time milliseconds it took.
        the measurement is printed in the test stream and compared into previous
        result in the snaphost file.

        This method also prints a new line after the measurements.

        NOTE: if max_ms is defined, this line will fail, if the test took more than
        max_ms milliseconds.
        """
        before = time.time()
        rv = f()
        after = time.time()
        ms = (after-before)*1000
        if ms > max_ms:
            self.fail().tln(f"{(after - before) * 1000:.2f} ms > "
                            f"max {max_ms:.2f} ms! (failed)")
        else:
            self.ifloatln(ms, "ms")

        return rv

    def imsln(self, f):
        """
        runs the function f and measures the time milliseconds it took.
        the measurement is printed in the test stream and compared into previous
        result in the snaphost file.

        This method also prints a new line after the measurements.

        NOTE: unline tmsln(), this method never fails or marks a difference.
        """
        return self.tmsln(f, sys.maxsize)

    def timage(self, file, alt_text=None):
        """
        Adds a markdown image in the test stream (tested).

        Args:
            file: Path to the image file
            alt_text: Optional alt text for the image (defaults to filename)
        """
        if alt_text is None:
            alt_text = os.path.splitext(os.path.basename(file))[0]
        self.tln(f"![{alt_text}]({self.rel_path(file)})")
        return self

    def iimage(self, file, alt_text=None):
        """
        Adds a markdown image in the info stream (not tested).

        Like timage() but for diagnostic/info output. Changes in image paths
        are shown in 'new | old' format for AI review but don't fail tests.

        Useful for plots, charts, and visualizations that help understand test
        behavior but shouldn't cause test failure if they change.

        Args:
            file: Path to the image file
            alt_text: Optional alt text for the image (defaults to filename)

        Example:
            t.iimage("plots/accuracy_curve.png", "Training Accuracy")
        """
        if alt_text is None:
            alt_text = os.path.splitext(os.path.basename(file))[0]
        self.iln(f"![{alt_text}]({self.rel_path(file)})")
        return self

    def tlist(self, list, prefix=" * "):
        """
        Writes the list into test stream. By default, the list
        is prefixed by markdown ' * ' list expression.

        For example following call:

        ```python
        t.tlist(["a", "b", "c"])
        ```

        will produce:

         * a
         * b
         * c
        """
        for i in list:
            self.tln(f"{prefix}{i}")

    def ilist(self, list, prefix=" * "):
        """
        Writes the list into test stream. By default, the list
        is prefixed by markdown ' * ' list expression.

        For example following call:

        ```python
        t.tlist(["a", "b", "c"])
        ```

        will produce:

         * a
         * b
         * c
        """
        for i in list:
            self.iln(f"{prefix}{i}")

    def tset(self, items, prefix=" * "):
        """
        This method used to print and compare a set of items to expected set
        in out of order fashion. It will first scan the next elements
        based on prefix. After this step, it will check whether the items
        were in the list.

        NOTE: this method may be slow, if the set order is unstable.
        """
        compare = None

        if self.exp_line is not None:
            begin = self.exp_line_number
            compare = set()
            while (self.exp_line is not None
                   and self.exp_line.startswith(prefix)):
                compare.add(self.exp_line[len(prefix):])
                self.next_exp_line()
            end = self.exp_line_number

        for i in items:
            i_str = str(i)
            line = f"{prefix}{i_str}"
            if compare is not None:
                if i_str in compare:
                    self.seek_line(line, begin, end)
                    compare.remove(i_str)
                else:
                    self.diff()
            self.iln(line)

        if compare is not None:
            if len(compare) > 0:
                self.diff()
            self.jump(end)

    def must_apply(self, it, title, cond, error_message=None):
        """
        Assertions with decoration for testing, whether `it`
        fulfills a condition.

        Maily used by TestIt class
        """
        prefix = f" * MUST {title}..."
        self.i(prefix).assertln(cond(it), error_message)

    def must_contain(self, it, member):
        """
        Assertions with decoration for testing, whether `it`
        contains a member.

        Maily used by TestIt class
        """
        self.must_apply(it, f"have {member}", lambda x: member in x)

    def must_equal(self, it, value):
        """
        Assertions with decoration for testing, whether `it`
        equals something.

        Maily used by TestIt class
        """
        self.must_apply(it, f"equal {value}", lambda x: x == value)

    def must_be_a(self, it, typ):
        """
        Assertions with decoration for testing, whether `it`
        is of specific type.

        Maily used by TestIt class
        """
        self.must_apply(it,
                        f"be a {typ}",
                        lambda x: type(x) == typ,
                        f"was {type(it)}")

    def it(self, name, it):
        """
        Creates TestIt class around the `it` object named with `name`

        This can be used for assertions as in:

        ```python
        result = [1, 2]
        t.it("result", result).must_be_a(list).must_contain(1).must_contain(2)
        ```
        """
        from booktest.reporting.testing import TestIt
        return TestIt(self, name, it)

    def tformat(self, value):
        """
        Converts the value into json like structure containing only the value types.

        Prints a json containing the value types.

        Mainly used for getting snapshot of a e.g. Json response format.
        """
        from booktest.reporting.testing import value_format
        self.tln(json.dumps(value_format(value), indent=2))
        return self

    def key(self, key):
        """Override key() to add anchor() functionality specific to TestCaseRun."""
        return self.anchor(key).i(" ")

    def ifloatln(self, value: float, unit: str = None):
        """
        Write a float value as info with optional delta from previous value.
        Built on i() and iln() primitives, using _get_expected_token() for comparison.

        If a previous value exists in snapshot, shows: "0.850 (was 0.820)"
        Otherwise shows: "0.850"

        Args:
            value: Float value to display
            unit: Optional unit string (e.g., "%", "ms")

        Example:
            t.ifloatln(0.973, "%")  # Output: "0.973% (was 0.950%)"
        """
        old = self._get_expected_token()
        try:
            old_value = float(old) if old is not None else None
        except ValueError:
            old_value = None

        postfix = f" {unit}" if unit else ""

        self.i(f"{value:.3f}{postfix}")
        if old_value is not None:
            self.iln(f" (was {old_value:.3f}{postfix})")
        else:
            self.iln()
        return self

    def ivalueln(self, value: Any, unit: str = None):
        """
        Write any value as info with optional delta from previous value.
        Built on i() and iln() primitives, using _get_expected_token() for comparison.

        If a previous value exists in snapshot, shows: "42 (was 38)"
        Otherwise shows: "42"

        Args:
            value: Value to display (converted to string)
            unit: Optional unit string (e.g., "items", "users")

        Example:
            t.ivalueln(1000, "users")  # Output: "1000 users (was 950 users)"
        """
        old = self._get_expected_token()

        postfix = f" {unit}" if unit else ""

        self.i(f"{value}{postfix}")
        if old is not None:
            self.iln(f" (was {old}{postfix})")
        else:
            self.iln()
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
            if error_message:
                self.failln(error_message)
            else:
                self.failln("FAILED")
        return self

    def _table(self, df: Any, feed_fn):
        """
        Internal helper to write a markdown table using a feed function.

        Args:
            df: pandas DataFrame or compatible object with .columns and .index
            feed_fn: Function to use for writing content (self.t or self.i)
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
        feed_fn(buf)
        feed_fn("\n")

        # Write separator row
        buf = "|"
        for i in pads:
            buf += "-" * i
            buf += "|"
        feed_fn(buf)
        feed_fn("\n")

        # Write data rows
        for i in df.index:
            feed_fn("|")
            for j, column in enumerate(df.columns):
                buf = str(df[column][i])\
                          .replace("\r", " ")\
                          .replace("\n", " ")\
                          .strip()

                feed_fn(buf)
                # Use i() for padding to keep it as info in both tested and info tables
                self.i(" " * (pads[j]-len(buf)))
                feed_fn("|")
            feed_fn("\n")

        return self

    def ttable(self, table: dict):
        """
        Write a markdown table from a dictionary of columns (tested).
        Built on _table() helper.

        Example:
            t.ttable({"x": [1, 2, 3], "y": [2, 3, 4]})
        """
        import pandas as pd
        return self.tdf(pd.DataFrame(table))

    def tdf(self, df: Any):
        """
        Write a pandas dataframe as a markdown table (tested).
        Built on _table() helper and t() primitive.

        Args:
            df: pandas DataFrame or compatible object with .columns and .index
        """
        return self._table(df, self.t)

    def itable(self, table: dict):
        """
        Write a markdown table from a dictionary of columns (info - not tested).
        Built on _table() helper.

        Like ttable() but for diagnostic/info output. Changes in table content
        are shown in 'new | old' format for AI review but don't fail tests.

        Example:
            t.itable({"metric": ["accuracy", "f1"], "value": [0.95, 0.92]})
        """
        import pandas as pd
        return self.idf(pd.DataFrame(table))

    def idf(self, df: Any):
        """
        Write a pandas dataframe as a markdown table (info - not tested).
        Built on _table() helper and i() primitive.

        Like tdf() but for diagnostic/info output. Changes in DataFrame content
        are shown in 'new | old' format for AI review but don't fail tests.

        Args:
            df: pandas DataFrame or compatible object with .columns and .index
        """
        return self._table(df, self.i)

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

    def tmetricln(self, value: float, tolerance: float, unit: str = None, direction: str = None):
        """
        Test a metric value with tolerance for acceptable variation, ending with newline.

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
            t.tmetricln(0.973, tolerance=0.02)  # Accuracy ±2%
            t.tmetricln(97.3, tolerance=2, unit="%")  # Same, with units
            t.tmetricln(0.973, tolerance=0.02, direction=">=")  # Only fail on drops
            t.tmetricln(latency_ms, tolerance=5, unit="ms", direction="<=")  # No increases

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

            diff = exceeds_tolerance or violates_direction

            # Mark as failed if tolerance or direction violated
            if diff:
                if delta > 0:
                    delta_str += f">{tolerance:.3f}!"
                else:
                    delta_str += f"<{tolerance:.3f}!"
                self.t(f"{value:.3f}{unit_str}")
            else:
                self.i(f"{value:.3f}{unit_str}")

            self.iln(f" (was {old_value:.3f}{unit_str}, Δ{delta_str}{unit_str})")

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
                self.t(f"{value:.3f}{unit_str}")
            else:
                self.i(f"{value:.3f}{unit_str}")

            self.iln(f" (was {old_value:.3f}{unit_str}, Δ{delta_str}{unit_str} [{delta_pct_str}])")

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

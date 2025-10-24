import hashlib
import logging
import os.path as path
import os

import time
import shutil

import sys
import json

from booktest.reporting.review import report_case_begin, case_review, report_case_result, maybe_print_logs
from booktest.llm.tokenizer import TestTokenizer, BufferIterator
from booktest.reporting.reports import TestResult, TwoDimensionalTestResult, SuccessState, SnapshotState
from booktest.utils.utils import file_or_resource_exists, open_file_or_resource
from booktest.config.naming import to_filesystem_path, from_filesystem_path
from booktest.reporting.output import OutputWriter
from booktest.reporting.colors import yellow, red, gray, cyan


class TestCaseRun(OutputWriter):
    """
    A utility, that manages an invidiual test run, and provides the
    main API for the test case
    """
    def __init__(self,
                 run,
                 test_path,
                 config,
                 output):
        # test_path may be in pytest format (with ::) or legacy format
        # Store both display name and filesystem-safe path
        self.test_path = test_path  # Display name (pytest format or legacy)
        self.test_path_fs = to_filesystem_path(test_path)  # Filesystem-safe path

        # Split using filesystem path for file operations
        relative_dir, name = path.split(self.test_path_fs)

        # name & context
        self.run = run
        self.name = name

        # configuration
        self.always_interactive = config.get("always_interactive", False)
        self.interactive = config.get("interactive", self.always_interactive)
        self.verbose = config.get("verbose", False)
        self.resource_snapshots = config.get("resource_snapshots", False)
        self.point_error_pos = config.get("point_error_pos", False)
        self.config = config

        if output is None:
            output = sys.stdout
        self.output = output

        # snapshot file (todo: change expectation jargon into snapshot jargon)
        self.exp_base_dir = path.join(run.exp_dir, relative_dir)
        os.system(f"mkdir -p {self.exp_base_dir}")
        self.exp_file_name = path.join(self.exp_base_dir, name + ".md")
        self.exp_dir_name = path.join(self.exp_base_dir, name)
        self.exp_file_exists = file_or_resource_exists(self.exp_file_name, self.resource_snapshots)
        self.exp = None
        self.exp_line = None
        self.exp_line_number = None
        self.exp_tokens = None

        # prepare output
        self.out_base_dir = path.join(run.out_dir, relative_dir)
        os.system(f"mkdir -p {self.out_base_dir}")
        self.out_file_name = path.join(self.out_base_dir, name + ".md")
        self.out_dir_name = path.join(self.out_base_dir, name)
        self.out_tmp_dir_name = path.join(self.out_base_dir, name + ".tmp")
        self.out = None
        self.out_line = ""

        # prepare reporting
        self.rep_file_name = path.join(self.out_base_dir, name + ".txt")
        self.rep = None

        # prepare std error output
        self.err_file_name = path.join(self.out_base_dir, name + ".log")

        # snapshot usage tracking
        self.snapshot_usage = {}  # Track snapshot usage for reporting

        # storage initialization
        self.storage = self._init_storage()
        # Use filesystem path for storage (DVC manifest keys must be filesystem-safe)
        self.test_id = self.test_path_fs

        self.err = None
        self.orig_err = None

        # prepare logging
        self.log = None
        self.orig_handlers = None

        # swap error
        self.orig_err = sys.stderr
        sys.stderr = self.err

        # error management
        #
        # let's separate diff from proper failure
        #
        # Token-level tracking: list of (position, marker_type) tuples
        # marker_type can be: 'diff', 'fail', 'info'
        self.line_markers = []  # [(pos, 'diff'), (pos, 'fail'), (pos, 'info')]

        # Legacy single-position tracking (for backward compatibility)
        self.line_diff = None
        self.line_error = None

        self.line_number = 0
        self.diffs = 0
        self.errors = 0
        self.info_diffs = 0  # Track info-level differences
        # this is needed for sensible default behavior, when sections end
        self.last_checked = False

        # reporting
        self.took_ms = None
        self.result = None

        # purge old output files
        if path.exists(self.out_dir_name):
            shutil.rmtree(self.out_dir_name)

        if path.exists(self.out_tmp_dir_name):
            shutil.rmtree(self.out_tmp_dir_name)

    def print(self, *args, sep=' ', end='\n'):
        print(*args, sep=sep, end=end, file=self.output)

    def report(self, *args, sep=' ', end='\n'):
        """ writes a report line in report log and possibly in standard output  """
        print(*args, sep=sep, end=end, file=self.rep)
        if self.verbose:
            self.print(*args, sep=sep, end=end)

    def reset_exp_reader(self):
        """ Resets the reader that reads expectation / snapshot file """
        self.close_exp_reader()
        if self.exp_file_exists:
            self.exp = open_file_or_resource(self.exp_file_name, self.resource_snapshots)
        else:
            self.exp = None
        self.exp_line = None
        self.exp_line_number = 0
        self.exp_tokens = None
        self.next_exp_line()

    def tmp_path(self, name):
        """
        creates a temporary file with the filename in the test's .tmp directory

        these files get deleted before new runs, and by `booktest --clean` command
        """
        if not path.exists(self.out_tmp_dir_name):
            os.mkdir(self.out_tmp_dir_name)
        return path.join(self.out_tmp_dir_name, name)

    def tmp_dir(self, dir_name):
        rv = self.tmp_path(dir_name)
        os.mkdir(rv)
        return rv

    def tmp_file(self, filename):
        return self.tmp_path(filename)

    def file(self, filename):
        """
        creates a file with the filename in the test's main directory

        these files can include test output or e.g. images and graphs included in the
        .md output. NOTE: these files may end up in Git, so keep them small
        and avoid sensitive information.
        """
        # prepare new output files
        if not path.exists(self.out_dir_name):
            os.mkdir(self.out_dir_name)
        return path.join(self.out_dir_name, filename)

    def start_review(self, llm=None):
        """
        Start an LLM-assisted review session.

        Returns an LlmReview instance that accumulates output and can use an LLM
        to answer questions about the test results.

        Args:
            llm: Optional Llm instance. If None, uses get_llm() default.

        Returns:
            LlmReview: Review instance for writing output and performing LLM-based validation

        Example:
            def test_code_generation(t: bt.TestCaseRun):
                r = t.start_review()

                r.h1("Generated Code:")
                r.icode(code, "python")

                r.start_review()
                r.reviewln("Is code well formatted?", "Yes", "No")

        For GPT/Azure OpenAI (default LLM), requires:
            - openai package
            - Environment variables: OPENAI_API_KEY, OPENAI_API_BASE, etc.
        """
        from booktest.llm.llm_review import LlmReview
        return LlmReview(self, llm=llm)

    def rename_file_to_hash(self, file, postfix=""):
        """
        this can be useful with images or similar resources it avoids overwrites
        (e.g. image.png won't be renamed with image.pnh), guarantees uniqueness
        and makes the test break whenever image changes.
        """
        with open(file, 'rb', buffering=0) as f:
            sha1 = hashlib.sha1()  # Create a SHA-1 hash object
            with open(file, "rb") as f:
                # Read the file in chunks to avoid memory issues with large files
                for chunk in iter(lambda: f.read(4096), b""):
                    sha1.update(chunk)
            hash_code = str(sha1.hexdigest())

            path, filename = os.path.split(file)
            name = os.path.join(path, hash_code + postfix)
            os.rename(file, name)
            return name

    def rel_path(self, file):
        """
        rel_path returns relative path for a file. the returned path that can be referred
        from the MD file e.g. in images
        """
        abs_file = os.path.abspath(file)
        abs_out_base_dir = os.path.abspath(self.out_base_dir)
        if abs_file[:len(abs_out_base_dir)] == abs_out_base_dir:
            return abs_file[len(abs_out_base_dir)+1:]
        else:
            return None

    def start(self, title=None):
        """
        Internal method: starts the test run with the given title
        """
        # open resources and swap loggers and stderr
        self.open()
        self.reset_exp_reader()

        self.started = time.time()
        report_case_begin(self.print,
                          self.test_path,
                          title,
                          self.verbose)

    def review(self, result):
        """
        Internal method: runs the review step, which is done at the end of the test.
        This method is typically called by end method()

        This step may be interactive depending on the configuration. It ends up with
        the user or automation accepting or rejecting the result.

        Returns test result (TEST, DIFF, OK) and interaction value, which is used to signal e.g.
        test run termination.
        """
        return case_review(
            self.exp_base_dir,
            self.out_base_dir,
            self.name,
            result,
            self.config)

    def end(self):
        """
        Test ending step. This records the test time, closes resources,
        and sets up preliminary result (FAIL, DIFF, OK). This also
        reports the case and calls the review step.

        :return: (result, interaction) where result can be legacy TestResult or TwoDimensionalTestResult
        """
        self.ended = time.time()
        self.took_ms = 1000*(self.ended - self.started)

        self.close()

        # Determine success state based on test logic
        if self.errors != 0:
            success_state = SuccessState.FAIL
            legacy_result = TestResult.FAIL
        elif self.diffs != 0 or not path.exists(self.exp_file_name):
            success_state = SuccessState.DIFF
            legacy_result = TestResult.DIFF
        else:
            success_state = SuccessState.OK
            legacy_result = TestResult.OK

        # Determine snapshot state from actual usage tracking
        snapshot_state = self.get_snapshot_state()

        # Note: snapshot_state reflects snapshot system operation (INTACT/UPDATED/FAIL)
        # It's independent of test success - snapshots can be successfully updated
        # even when test assertions fail

        # Create two-dimensional result
        two_dim_result = TwoDimensionalTestResult(
            success=success_state,
            snapshotting=snapshot_state
        )

        # Use two-dimensional result for reporting if available, fall back to legacy
        display_result = two_dim_result if two_dim_result else legacy_result

        maybe_print_logs(self.print, self.config, self.out_base_dir, self.name)

        report_case_result(
            self.print,
            self.test_path,
            display_result,
            self.took_ms,
            self.verbose)

        # Pass two-dimensional result to review for proper snapshot handling
        rv, interaction, ai_result = self.review(two_dim_result)

        if self.verbose:
            self.print("")

        # Store both results for future use
        self.result = rv
        self.two_dimensional_result = two_dim_result

        # Write snapshot metadata to separate file
        if self.snapshot_usage:
            metadata_file = self.file("_snapshots/metadata.json")
            metadata_dir = path.dirname(metadata_file)
            os.makedirs(metadata_dir, exist_ok=True)

            import json
            with open(metadata_file, 'w') as f:
                json.dump({
                    'test_id': self.test_path,
                    'snapshots': self.snapshot_usage,
                    'result': {
                        'success': success_state.value,
                        'snapshotting': snapshot_state.value
                    },
                    'timestamp': time.time()
                }, f, indent=2)

        return rv, interaction, ai_result

    def report_snapshot_usage(self,
                              snapshot_type: str,
                              hash_value: str,
                              state: SnapshotState,
                              details: dict = None):
        """
        Report snapshot usage for this test.

        Args:
            snapshot_type: Type of snapshot (http, httpx, env, func)
            hash_value: SHA256 hash of snapshot content
            state: Current state (INTACT, UPDATED, FAIL)
            details: Optional additional information about the snapshot
        """
        self.snapshot_usage[snapshot_type] = {
            'hash': hash_value,
            'state': state.value,
            'details': details or {},
            'timestamp': time.time()
        }

    def get_snapshot_state(self) -> SnapshotState:
        """
        Determine overall snapshot state from tracked usage.

        Returns:
            SnapshotState: INTACT if all snapshots valid, UPDATED if any updated,
                          FAIL if any failed
        """
        if not self.snapshot_usage:
            return SnapshotState.INTACT

        states = [SnapshotState(u['state'])
                 for u in self.snapshot_usage.values()]

        # If any snapshot failed, overall state is FAIL
        if any(s == SnapshotState.FAIL for s in states):
            return SnapshotState.FAIL

        # If any snapshot was updated, overall state is UPDATED
        if any(s == SnapshotState.UPDATED for s in states):
            return SnapshotState.UPDATED

        # All snapshots intact
        return SnapshotState.INTACT

    def _init_storage(self):
        """
        Initialize storage backend based on configuration.

        Returns:
            SnapshotStorage: Configured storage instance (GitStorage or DVCStorage)
        """
        from booktest.snapshots.storage import GitStorage, DVCStorage

        mode = self.config.get("storage.mode", "git")

        # Use out_dir for writing (staging), exp_dir for reading (frozen)
        # GitStorage will handle both locations
        # For parallel runs, pass batch_dir to avoid manifest race conditions
        batch_dir = self.run.batch_dir if hasattr(self.run, 'batch_dir') else None

        if mode == "auto":
            # Auto-detect: use DVC if available, otherwise Git
            if DVCStorage.is_available():
                return DVCStorage(
                    base_path=self.run.out_dir,  # Write to .out
                    remote=self.config.get("storage.dvc.remote", "booktest-remote"),
                    manifest_path=self.config.get("storage.dvc.manifest_path", "booktest.manifest.yaml"),
                    batch_dir=batch_dir
                )
            return GitStorage(base_path=self.run.out_dir, frozen_path=self.run.exp_dir)
        elif mode == "dvc":
            return DVCStorage(
                base_path=self.run.out_dir,  # Write to .out
                remote=self.config.get("storage.dvc.remote", "booktest-remote"),
                manifest_path=self.config.get("storage.dvc.manifest_path", "booktest.manifest.yaml"),
                batch_dir=batch_dir
            )
        else:  # mode == "git" or fallback
            return GitStorage(base_path=self.run.out_dir, frozen_path=self.run.exp_dir)

    def get_storage(self):
        """
        Get the storage backend for this test.

        Returns:
            SnapshotStorage: The storage instance
        """
        return self.storage

    def close_exp_reader(self):
        """
        Closes the expectation/snapshot file reader
        :return:
        """

        if self.exp is not None:
            self.exp.close()
            self.exp = None

    def open(self):
        # open files
        self.out = open(self.out_file_name, "w")
        self.rep = open(self.rep_file_name, "w")
        self.err = open(self.err_file_name, "w")
        self.log = logging.StreamHandler(self.err)

        # swap logger
        logger = logging.getLogger()
        self.orig_handlers = logger.handlers

        formatter = None
        if len(self.orig_handlers) > 0:
            formatter = self.orig_handlers[0].formatter
            self.log.setFormatter(formatter)

        logger.handlers = [self.log]

        # swap logging
        self.orig_err = sys.stderr
        sys.stderr = self.err


    def close(self):
        """
        Closes all resources (e.g. file system handles).
        """
        if self.orig_handlers is not None:
            logger = logging.getLogger()
            logger.handlers = self.orig_handlers
            self.orig_handlers = None

        if self.log is not None:
            self.log.close()
            self.log = None

        if self.orig_err is not None:
            sys.stderr = self.orig_err
            self.orig_err = None

        self.err.close()
        self.err = None

        self.close_exp_reader()
        self.out.close()
        self.out = None
        self.rep.close()
        self.rep = None

    def next_exp_line(self):
        """
        Moves snapshot reader cursor to the next snapshot file line
        """
        if self.exp_file_exists:
            if self.exp:
                line = self.exp.readline()
                if len(line) == 0:
                    self.close_exp_reader()
                    self.exp_line = None
                    self.exp_tokens = None
                    self.exp_line_number += 1
                else:
                    self.exp_line_number += 1
                    self.exp_line = line[0:len(line)-1]
                    self.exp_tokens =\
                        BufferIterator(TestTokenizer(self.exp_line))
            elif self.last_checked:
                self.exp_line = None
                self.exp_tokens = None

    def jump(self, line_number):
        """
        Moves the snapshot reader cursor to the specified line number.

        If line number is before current reader position, the snapshot
        file reader is reset.
        """
        if self.exp_file_exists:

            if line_number < self.exp_line_number:
                self.reset_exp_reader()

            while (self.exp_line is not None
                   and self.exp_line_number < line_number):
                self.next_exp_line()

    def seek(self, is_line_ok, begin=0, end=sys.maxsize):
        """
        Seeks the next snapshot/expectation file line that matches the
        is_line_ok() lambda. The seeking is started on 'begin' line and
        it ends on the 'end' line.

        NOTE: The seeks starts from the cursor position,
        but it may restart seeking from the beginning of the file,
        if the sought line is not found.

        NOTE: this is really an O(N) scanning operation.
              it may restart at the beginning of file and
              it typically reads the the entire file
              on seek failures.
        """
        if self.exp_file_exists:
            at_line_number = self.exp_line_number

            # scan, until the anchor is found
            while (self.exp_line is not None
                   and not is_line_ok(self.exp_line)
                   and self.exp_line_number < end):
                self.next_exp_line()
            if self.exp_line is None:
                # if anchor was not found, let's look for previous location
                # or alternatively: let's return to the original location
                self.jump(begin)
                while (self.exp_line is not None
                       and not is_line_ok(self.exp_line)
                       and self.exp_line_number < at_line_number):
                    self.next_exp_line()

    def seek_line(self, anchor, begin=0, end=sys.maxsize):
        """
        Seeks the next snapshot/expectation file line matching the anchor.

        NOTE: The seeks starts from the cursor position,
        but it may restart seeking from the beginning of the file,
        if the sought line is not found.

        NOTE: this is really an O(N) scanning operation.
              it may restart at the beginning of file and
              it typically reads the the entire file
              on seek failures.
        """
        return self.seek(lambda x: x == anchor, begin, end)

    def seek_prefix(self, prefix):
        """
        Seeks the next snapshot/expectation file line matching the prefix.

        NOTE: The seeks starts from the cursor position,
        but it may restart seeking from the beginning of the file,
        if the sought line is not found.

        NOTE: this is really an O(N) scanning operation.
              it may restart at the beginning of file and
              it typically reads the the entire file
              on seek failures.
        """
        return self.seek(lambda x: x.startswith(prefix))

    def write_line(self):
        """
        Internal method. Writes a line into test output file and moves
        the snaphost line forward by one.
        """
        self.out.write(self.out_line)
        self.out.write('\n')
        self.out.flush()
        self.out_line = ""
        self.next_exp_line()
        self.line_number = self.line_number + 1

    def commit_line(self):
        """
        Internal method. Commits the prepared line into testing.

        This writes both decorated line into reporting AND this writes
        the line into test output. Also the snapshot file cursor is
        moved into next line.

        Statistics line number of differing or erroneous lines get
        updated.

        Uses token-level markers for fine-grained coloring of specific
        tokens/cells that changed, failed, or have info-level differences.
        """

        # Check if there are any markers on this line
        has_token_markers = len(self.line_markers) > 0
        has_line_markers = self.line_error is not None or self.line_diff is not None

        if has_line_markers or has_token_markers:
            # Determine line-level symbol and update stats
            # Markers are (start_pos, end_pos, marker_type) tuples
            has_error = self.line_error is not None or any(m[2] == 'fail' for m in self.line_markers)
            has_diff = self.line_diff is not None or any(m[2] == 'diff' for m in self.line_markers)
            has_info = any(m[2] == 'info' for m in self.line_markers)

            symbol = "?"
            pos = None

            if has_error:
                symbol = "!"
                self.errors += 1
                pos = self.line_error if self.line_error is not None else 0
            elif has_diff:
                symbol = "?"
                self.diffs += 1
                pos = self.line_diff if self.line_diff is not None else 0
            elif has_info:
                symbol = "."
                self.info_diffs += 1
                pos = 0

            # Choose coloring approach based on markers
            if has_token_markers and len(self.line_markers) > 0:
                # Use token-level coloring
                try:
                    colored_line = self._colorize_line_with_markers(
                        self.out_line, self.line_markers,
                        has_error, has_diff, has_info
                    )
                    # Color the symbol itself
                    if has_error:
                        colored_symbol = red(symbol)
                    elif has_diff:
                        colored_symbol = yellow(symbol)
                    else:
                        colored_symbol = cyan(symbol)
                    # Pad the uncolored line to 60 chars, then apply coloring
                    # We need to pad before coloring to get correct alignment
                    padded_line = f"{self.out_line:60s}"
                    # Now colorize the padded content
                    colored_padded = self._colorize_line_with_markers(
                        padded_line, self.line_markers,
                        has_error, has_diff, has_info
                    )
                    left_side = f"{colored_symbol} {colored_padded}"
                except Exception as e:
                    # Fallback to line-level coloring on error
                    import traceback
                    import sys
                    print(f"Warning: token coloring failed: {e}", file=sys.stderr)
                    traceback.print_exc(file=sys.stderr)
                    if has_error:
                        color_fn = red
                    elif has_diff:
                        color_fn = yellow
                    else:
                        color_fn = cyan
                    left_side = color_fn(f"{symbol} {self.out_line:60s}")
            else:
                # Use line-level coloring
                if has_error:
                    color_fn = red
                elif has_diff:
                    color_fn = yellow
                else:
                    color_fn = cyan
                left_side = color_fn(f"{symbol} {self.out_line:60s}")

            if self.exp_line is not None:
                # Colorize expected line with differing tokens highlighted
                right_side = self._colorize_expected_line(self.exp_line, self.line_markers)
                self.report(f"{left_side} | {right_side}")
            else:
                right_side = gray("EOF")
                self.report(f"{left_side} | {right_side}")

            if self.point_error_pos:
                self.report("  " + (" " * pos) + "^")

            self.write_line()

            # Clear markers for next line
            self.line_markers = []
            self.line_error = None
            self.line_diff = None
        else:
            self.report(f"  {self.out_line}")
            self.write_line()

    def _colorize_line_with_markers(self, line, markers, has_error, has_diff, has_info):
        """
        Colorize a line using token-level markers.

        Args:
            line: The line text to colorize
            markers: List of (start_pos, end_pos, marker_type) tuples
            has_error: True if line has any error markers
            has_diff: True if line has any diff markers
            has_info: True if line has any info markers

        Returns:
            Colored string with ANSI color codes
        """
        from booktest.reporting.colors import yellow, red, cyan

        if not markers:
            # No markers - use line-level coloring (fallback)
            if has_error:
                return red(line)
            elif has_diff:
                return yellow(line)
            elif has_info:
                return cyan(line)
            return line

        # Sort markers by start position and deduplicate
        # Filter out invalid positions
        valid_markers = [(start, end, mtype) for start, end, mtype in markers
                        if 0 <= start <= len(line) and 0 <= end <= len(line)]
        if not valid_markers:
            # Fallback to line-level coloring
            if has_error:
                return red(line)
            elif has_diff:
                return yellow(line)
            elif has_info:
                return cyan(line)
            return line

        sorted_markers = sorted(set(valid_markers), key=lambda m: m[0])

        # Build colored line token by token
        result = ""
        last_pos = 0

        for start_pos, end_pos, marker_type in sorted_markers:
            # Add uncolored text before this marker
            if start_pos > last_pos:
                result += line[last_pos:start_pos]

            # Colorize the token based on marker type
            token = line[start_pos:end_pos]
            if marker_type == 'fail':
                result += red(token)
            elif marker_type == 'diff':
                result += yellow(token)
            elif marker_type == 'info':
                result += cyan(token)
            else:
                result += token

            last_pos = end_pos

        # Add any remaining uncolored text
        if last_pos < len(line):
            result += line[last_pos:]

        return result

    def _colorize_expected_line(self, exp_line, markers):
        """
        Colorize the expected line by highlighting differing tokens.

        The base text is shown in dim gray (more subtle than regular gray), while tokens
        that differ from the new output are shown in regular gray for contrast.

        Args:
            exp_line: The expected line text
            markers: List of (start_pos, end_pos, marker_type) tuples from the output line

        Returns:
            Colored string with differing tokens highlighted
        """
        from booktest.reporting.colors import dim_gray, gray
        from booktest.llm.tokenizer import TestTokenizer

        if not markers or not exp_line:
            return dim_gray(exp_line)

        # Tokenize both lines to find corresponding positions
        out_tokens = list(TestTokenizer(self.out_line))
        exp_tokens = list(TestTokenizer(exp_line))

        # Build list of token positions in expected line that differ
        differing_positions = set()
        out_pos = 0
        exp_pos = 0

        for i, out_token in enumerate(out_tokens):
            # Check if this output token has a marker
            has_marker = any(start <= out_pos < end for start, end, _ in markers)

            if i < len(exp_tokens):
                exp_token = exp_tokens[i]
                if has_marker and out_token != exp_token:
                    # Mark this position in expected line as differing
                    differing_positions.add((exp_pos, exp_pos + len(exp_token)))
                exp_pos += len(exp_token)

            out_pos += len(out_token)

        # Build the colored expected line
        if not differing_positions:
            return dim_gray(exp_line)

        result = ""
        last_pos = 0
        sorted_positions = sorted(differing_positions)

        for start, end in sorted_positions:
            # Add dim gray text before this differing token
            if start > last_pos:
                result += dim_gray(exp_line[last_pos:start])

            # Highlight the differing token in regular gray for contrast
            result += gray(exp_line[start:end])
            last_pos = end

        # Add remaining dim gray text
        if last_pos < len(exp_line):
            result += dim_gray(exp_line[last_pos:])

        return result

    def head_exp_token(self):
        """
        Returns the next token in the snapshot file without moving snapshot file cursor
        """
        if self.exp_tokens is not None:
            if self.exp_tokens.has_next():
                return self.exp_tokens.head
            else:
                return '\n'
        else:
            return None

    def next_exp_token(self):
        """
        Reads the next token from the snapshot file. NOTE: this moves snapshot file
        cursor into the next token.
        """
        if self.exp_tokens is not None:
            if self.exp_tokens.has_next():
                return next(self.exp_tokens)
            else:
                return '\n'
        else:
            return None

    def feed_token(self, token, check=False, info_check=False):
        """
        Feeds a token into test stream with optional comparison.

        Args:
            token: The token to feed
            check: If True, compare against snapshot and mark diff() on mismatch
            info_check: If True, compare against snapshot and mark info() on mismatch
                       (shows in diff without failing test)

        NOTE: if token is a line end character, the line will be committed
        to the test stream.
        """
        exp_token = self.next_exp_token()
        self.last_checked = check or info_check

        if token == '\n':
            self.commit_line()
        else:
            # Add markers after appending token so position is correct
            start_pos = len(self.out_line)
            self.out_line = self.out_line + token

            if self.exp_file_exists and token != exp_token:
                if check:
                    # Tested content: mark as diff (fails test)
                    # Mark with token length info: (start_pos, end_pos, marker_type)
                    self.line_markers.append((start_pos, len(self.out_line), 'diff'))
                    if self.line_diff is None:
                        self.line_diff = start_pos
                elif info_check:
                    # Info content: mark as info (shows in diff, doesn't fail)
                    self.line_markers.append((start_pos, len(self.out_line), 'info'))
        return self

    def test_feed_token(self, token):
        """
        Feeds a token into test stream. The token will be compared to the next
        awaiting token in the snapshot file, and on difference a 'diff' is reported.
        """
        self.feed_token(token, check=True)
        return self

    def info_feed_token(self, token):
        """
        Feeds a token into info stream. The token will be compared to the next
        awaiting token in the snapshot file, but differences are marked as 'info'
        (shown in diff without causing test failure).
        """
        self.feed_token(token, info_check=True)
        return self

    def test_feed(self, text):
        """
        Feeds a piece text into the test stream. The text tokenized and feed
        into text stream as individual tokens.

        NOTE: The token content IS COMPARED to snapshot content for differences
        that are reported.
        """
        tokens = TestTokenizer(str(text))
        for t in tokens:
            self.test_feed_token(t)
        return self

    def feed(self, text):
        """
        Feeds a piece text into the info stream. The text tokenized and feed
        into text stream as individual tokens.

        NOTE: The token content IS NOT COMPARED to snapshot content, and differences
        are ignored
        """
        tokens = TestTokenizer(text)
        for t in tokens:
            self.feed_token(t)
        return self

    def info_feed(self, text):
        """
        Feeds a piece text into the info stream with comparison. The text is tokenized
        and compared to snapshot content. Differences are marked as 'info' (shown in
        diff without causing test failure).

        Use this for diagnostic output that should be tracked but not cause failures.
        """
        tokens = TestTokenizer(str(text))
        for t in tokens:
            self.info_feed_token(t)
        return self

    def diff(self):
        """
        Mark the entire current line as different.

        This marks a difference at the current position and sets the legacy
        line_diff marker for the whole line.
        """
        if self.line_diff is None:
            self.line_diff = len(self.out_line)
        # Also add to token-level markers (mark from current pos to end of line)
        self.line_markers.append((len(self.out_line), len(self.out_line), 'diff'))
        return self

    def diff_token(self):
        """
        Mark only the current token/position as different.

        Use this for fine-grained diff marking, e.g., to highlight a specific
        changed cell in a table without marking the entire row as different.

        Note: This should be called AFTER adding the token to out_line to properly
        capture the token length. Prefer using feed_token with check=True.
        """
        pos = len(self.out_line)
        self.line_markers.append((pos, pos, 'diff'))
        # Update line-level marker if not set
        if self.line_diff is None:
            self.line_diff = pos
        return self

    def fail(self):
        """
        Mark the entire current line as failed.

        This marks a failure at the current position and sets the legacy
        line_error marker for the whole line.
        """
        if self.line_error is None:
            self.line_error = len(self.out_line)
        # Also add to token-level markers (mark from current pos to end of line)
        self.line_markers.append((len(self.out_line), len(self.out_line), 'fail'))
        return self

    def fail_token(self):
        """
        Mark only the current token/position as failed.

        Use this for fine-grained failure marking, e.g., to highlight a specific
        failed assertion in a table cell without marking the entire row as failed.

        Note: This should be called AFTER adding the token to out_line to properly
        capture the token length. Prefer using feed_token with check=True.
        """
        pos = len(self.out_line)
        self.line_markers.append((pos, pos, 'fail'))
        # Update line-level marker if not set
        if self.line_error is None:
            self.line_error = pos
        return self

    def info(self):
        """
        Mark the entire current line as having info-level differences.

        Info markers show differences in diagnostic output (i() content) that
        don't cause test failure. These appear in 'new | old' format for AI
        review context without marking the test as failed.
        """
        self.line_markers.append((len(self.out_line), len(self.out_line), 'info'))
        return self

    def info_token(self):
        """
        Mark only the current token/position as having info-level differences.

        Use this for fine-grained info marking, e.g., to highlight which specific
        cell in a diagnostic table changed without affecting the test result.

        Note: This should be called AFTER adding the token to out_line to properly
        capture the token length. Prefer using feed_token with info_check=True.
        """
        pos = len(self.out_line)
        self.line_markers.append((pos, pos, 'info'))
        return self

    def _get_expected_token(self):
        """
        Override to provide snapshot comparison capability for metric tracking.
        Returns the next token from snapshot without advancing cursor.
        """
        return self.head_exp_token()

    def anchor(self, anchor):
        """
        creates a prefix anchor by seeking & printing prefix. e.g. if you have "key=" anchor,
        the snapshot cursor will be moved to next line starting with "key=" prefix.

        This method is used for controlling the snapshot cursor location and guaranteeing
        that a section in test is compared against correct section in the snapshot
        """
        self.seek_prefix(anchor)
        self.t(anchor)
        return self

    def anchorln(self, anchor):
        """
        creates a line anchor by seeking & printing an anchor line. e.g. if you have "# SECTION 3" anchor,
        the snapshot cursor will be moved to next "# SECTION 3" line.

        This method is used for controlling the snapshot cursor location and guaranteeing
        that a section in test is compared against correct section in the snapshot
        """
        self.seek_line(anchor)
        self.tln(anchor)
        return self

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

    def ifloatln(self, value, unit = None):
        old = self.head_exp_token()
        try:
            if old is not None:
                old = float(old)
        except ValueError:
            old = None

        if unit is not None:
            postfix = f" {unit}"
        else:
            postfix = ""

        self.i(f"{value:.3f}{postfix}")
        if old is not None:
            self.iln(f" (was {old:.3f}{postfix})")
        else:
            self.iln()

    def ivalueln(self, value, unit = None):
        old = self.head_exp_token()

        if unit is not None:
            postfix = f" {unit}"
        else:
            postfix = ""

        self.i(f"{value}{postfix}")
        if old is not None:
            self.iln(f" (was {old}{postfix})")
        else:
            self.iln()

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

    def h(self, level: int, title: str):
        """
        Markdown style header (primitive method for OutputWriter).

        This method is used to mark titles. Use h1(), h2(), h3() convenience methods instead.

        ```python
        t.h1("This is my title")
        t.h2("Subsection")
        ```
        """
        self.header("#" * level + " " + title)
        return self

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
        return TestIt(self, name, it)

    def tformat(self, value):
        """
        Converts the value into json like structure containing only the value types.

        Prints a json containing the value types.

        Mainly used for getting snapshot of a e.g. Json response format.
        """
        self.tln(json.dumps(value_format(value), indent=2))
        return self

    def key(self, key):
        """Override key() to add anchor() functionality specific to TestCaseRun."""
        return self.anchor(key).i(" ")

    def keyvalueln(self, key, value):
        """
        Prints a value of format "{key} {value}", and uses key as prefix anchor for
        adjusting the snapshot file cursor.
        """
        return self.key(key).tln(value)

    def t(self, text):
        """
        Writes tested text inline (primitive method for OutputWriter).

        In TestCaseRun, this text is compared against snapshots.
        """
        self.test_feed(text)
        return self

    def i(self, text):
        """
        Writes info text inline (primitive method for OutputWriter).

        In TestCaseRun, differences in info content are marked with info markers
        (shown in diff without causing test failure).
        'i' comes from 'info'/'ignore'.
        """
        self.info_feed(text)
        return self


def value_format(value):
    value_type = type(value)
    if value_type is list:
        rv = []
        for item in value:
            rv.append(value_format(item))
    elif value_type is dict:
        rv = {}
        for key in value:
            rv[key] = value_format(value[key])
    else:
        rv = value_type.__name__
    return rv


class TestIt:
    """ utility for making assertions related to a specific object """

    def __init__(self, run: TestCaseRun, title: str, it):
        self.run = run
        self.title = title
        self.it = it
        run.h2(title + "..")

    def must_contain(self, member):
        self.run.must_contain(self.it, member)
        return self

    def must_equal(self, member):
        self.run.must_equal(self.it, member)
        return self

    def must_be_a(self, typ):
        self.run.must_be_a(self.it, typ)
        return self

    def must_apply(self, title, cond):
        self.run.must_apply(self.it, title, cond)
        return self

    def member(self, title, select):
        """ Creates a TestIt class for the member of 'it' """
        return TestIt(self.run, self.title + "." + title, select(self.it))


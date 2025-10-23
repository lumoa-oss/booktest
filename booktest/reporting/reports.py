import logging
import os
import json

from enum import Enum
from typing import NamedTuple


#
# Test results and CLI user interaction
#


class TestResult(Enum):
    """Legacy single-dimensional test result (for backward compatibility)"""
    OK = 1
    FAIL = 2
    DIFF = 3


class SuccessState(Enum):
    """Test logic outcome - independent of snapshot management"""
    OK = "ok"       # Test logic passed, output matches expectations
    DIFF = "diff"   # Test logic output differs, needs human review
    FAIL = "fail"   # Test logic failed (exceptions, assertions)


class SnapshotState(Enum):
    """Snapshot integrity outcome - independent of test logic"""
    INTACT = "intact"    # Snapshots are current and valid
    UPDATED = "updated"  # Snapshots were refreshed during this run
    FAIL = "fail"        # Snapshot mechanism failed


class TwoDimensionalTestResult(NamedTuple):
    """Two-dimensional test result separating logic success from snapshot management"""
    success: SuccessState
    snapshotting: SnapshotState

    def to_legacy_result(self) -> TestResult:
        """Convert to legacy single-dimensional result for backward compatibility"""
        if self.success == SuccessState.OK:
            return TestResult.OK
        elif self.success == SuccessState.DIFF:
            return TestResult.DIFF
        else:  # FAIL
            return TestResult.FAIL

    def requires_review(self) -> bool:
        """Check if this result requires human review"""
        return self.success == SuccessState.DIFF

    def is_success(self) -> bool:
        """Check if the test logic succeeded (regardless of snapshots)"""
        return self.success == SuccessState.OK

    def can_auto_approve(self) -> bool:
        """Check if this result can be auto-approved without human review"""
        return self.success == SuccessState.OK

    def __str__(self) -> str:
        """String representation for CLI display"""
        return f"{self.success.value.upper()}/{self.snapshotting.value.upper()}"


def test_result_to_exit_code(test_result):
    """Convert test result to exit code (supports both legacy and new format)"""
    if isinstance(test_result, TwoDimensionalTestResult):
        test_result = test_result.to_legacy_result()

    if test_result == TestResult.OK:
        return 0
    else:
        return -1


class UserRequest(Enum):
    NONE = 0
    ABORT = 1
    FREEZE = 2



#
# IO helper utilities
#


def write_lines(path, file, lines):
    file = os.path.join(path, file)
    with open(file, "w") as f:
        return f.write("\n".join(lines) + "\n")


def read_lines(path, filename=None):
    if filename is None:
        file = path
    else:
        file = os.path.join(path, filename)
    if os.path.exists(file):
        with open(file, "r") as f:
            rv = f.read().split("\n")
            if len(rv) > 0 and len(rv[len(rv)-1]) == 0:
                # remove empty trailing line
                rv = rv[:len(rv)-1]
            return rv
    else:
        return []


#
# Saved test reporting
#


class Metrics:
    """
    Stores the top level test metrics/results
    """

    def __init__(self, took_ms):
        self.took_ms = took_ms

    def to_file(self, path):
        with open(path, "w") as f:
            json.dump({
                "tookMs": self.took_ms
            }, f)

    @staticmethod
    def of_file(path):
        with open(path, "r") as f:
            state = json.load(f)
            return Metrics(state["tookMs"])

    def to_dir(self, dir):
        self.to_file(os.path.join(dir, "metrics.json"))

    @staticmethod
    def of_dir(dir):
        return Metrics.of_file(os.path.join(dir, "metrics.json"))


class CaseReports:
    """
    This class manages the saved case specific metrics/results.

    Supports both legacy text format (cases.txt) and new JSON format (cases.json).
    The JSON format includes AI review results which are invalidated when tests rerun.
    """

    def __init__(self, cases, ai_reviews=None):
        """
        Initialize CaseReports.

        Args:
            cases: List of (case_name, result, duration) tuples
            ai_reviews: Optional dict mapping case_name to AIReviewResult
        """
        self.cases = cases
        self.ai_reviews = ai_reviews if ai_reviews is not None else {}

    def passed(self):
        return [i[0] for i in self.cases if i[1] == TestResult.OK]

    def failed(self):
        return [i[0] for i in self.cases if i[1] != TestResult.OK]

    def failed_with_details(self):
        """Return failed test cases with their result type and duration."""
        return [(i[0], i[1], i[2]) for i in self.cases if i[1] != TestResult.OK]

    def by_name(self, name):
        return list([i for i in self.cases if i[0] == name])

    def get_ai_review(self, case_name):
        """Get AI review for a specific test case, if available."""
        return self.ai_reviews.get(case_name)

    def set_ai_review(self, case_name, ai_review):
        """
        Set AI review for a specific test case.

        Args:
            case_name: Test case name
            ai_review: AIReviewResult object or None to remove
        """
        if ai_review is None:
            self.ai_reviews.pop(case_name, None)
        else:
            self.ai_reviews[case_name] = ai_review

    def cases_to_done_and_todo(self, cases, config):
        cont = config.get("continue", False)
        if cont:
            done = []
            todo = []
            for i in cases:
                record = self.by_name(i)
                if len(record) > 0 and record[0][1] == TestResult.OK:
                    done.append(record[0])
                else:
                    todo.append(i)
            return done, todo
        else:
            return [], cases

    @staticmethod
    def of_dir(out_dir):
        """
        Load case reports from directory.

        Prefers cases.ndjson (NDJSON) if it exists, falls back to cases.txt for backward compatibility.
        """
        jsonl_file = os.path.join(out_dir, "cases.ndjson")
        txt_file = os.path.join(out_dir, "cases.txt")

        if os.path.exists(jsonl_file):
            return CaseReports.of_jsonl_file(jsonl_file)
        elif os.path.exists(txt_file):
            return CaseReports.of_file(txt_file)
        else:
            return CaseReports([])

    @staticmethod
    def of_file(file_name):
        cases = []
        for at, j in enumerate(read_lines(file_name)):
            if len(j.strip()) > 0:
                parts = j.split("\t")
                try:
                    case_name = parts[0]
                    result_str = parts[1]
                    if result_str == "OK":
                        result = TestResult.OK
                    elif result_str == "DIFF":
                        result = TestResult.DIFF
                    elif result_str == "FAIL":
                        result = TestResult.FAIL
                    else:
                        raise Exception(f"{result_str}?")

                    duration = float(parts[2])
                    cases.append((case_name,
                                  result,
                                  duration))
                except Exception as e:
                    logging.exception(f"parsing line {at}: '{j}' in {os.path.abspath(file_name)} failed with {e}")

        return CaseReports(cases)

    @staticmethod
    def write_case(file_handle,
                   case_name,
                   res: TestResult,
                   duration):
        file_handle.write(
            f"{case_name}\t{res.name}\t{duration}\n")
        file_handle.flush()

    @staticmethod
    def make_case(case_name,
                  res: TestResult,
                  duration):
        return (case_name, res, duration)

    def to_dir(self, out_dir):
        """Save case reports to directory (uses NDJSON format)."""
        jsonl_file = os.path.join(out_dir, "cases.ndjson")
        return self.to_jsonl_file(jsonl_file)

    def to_file(self, file):
        """Save to legacy text format (for backward compatibility)."""
        with open(file, "w") as f:
            for i in self.cases:
                CaseReports.write_case(f,
                                       i[0],
                                       i[1],
                                       i[2])

    @staticmethod
    def of_jsonl_file(file_name):
        """Load case reports from NDJSON file (newline-delimited JSON)."""
        if not os.path.exists(file_name):
            return CaseReports([])

        cases = []
        ai_reviews = {}

        try:
            with open(file_name, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        case_data = json.loads(line)
                        case_name = case_data['name']
                        result_str = case_data['result']

                        # Convert result string to TestResult enum
                        if result_str == "OK":
                            result = TestResult.OK
                        elif result_str == "DIFF":
                            result = TestResult.DIFF
                        elif result_str == "FAIL":
                            result = TestResult.FAIL
                        else:
                            logging.warning(f"Unknown result type: {result_str}, treating as FAIL")
                            result = TestResult.FAIL

                        duration = case_data.get('duration_ms', 0.0)
                        cases.append((case_name, result, duration))

                        # Load AI review if present
                        if 'ai_review' in case_data and case_data['ai_review'] is not None:
                            try:
                                from booktest.llm.llm_review import AIReviewResult
                                ai_review = AIReviewResult(**case_data['ai_review'])
                                ai_reviews[case_name] = ai_review
                            except Exception as e:
                                logging.warning(f"Failed to load AI review for {case_name}: {e}")

                    except json.JSONDecodeError as e:
                        logging.warning(f"Invalid JSON on line {line_num} of {file_name}: {e}")
                    except KeyError as e:
                        logging.warning(f"Missing required field {e} on line {line_num} of {file_name}")

            return CaseReports(cases, ai_reviews)

        except Exception as e:
            logging.exception(f"Error loading cases from {file_name}: {e}")
            return CaseReports([])

    def to_jsonl_file(self, file_name):
        """Save case reports to NDJSON file (newline-delimited JSON)."""
        import time

        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'w') as f:
            for case_name, result, duration in self.cases:
                case_entry = {
                    'name': case_name,
                    'result': result.name,
                    'duration_ms': duration,
                    'timestamp': time.time()
                }

                # Include AI review if available
                ai_review = self.ai_reviews.get(case_name)
                if ai_review is not None:
                    # Convert AIReviewResult to dict
                    from dataclasses import asdict
                    case_entry['ai_review'] = asdict(ai_review)
                else:
                    case_entry['ai_review'] = None

                # Write as single line JSON
                f.write(json.dumps(case_entry) + '\n')

        return self

    @staticmethod
    def write_case_jsonl(file_handle, case_name, res: TestResult, duration, ai_review=None):
        """Write a single case to NDJSON file."""
        import time
        from dataclasses import asdict

        case_entry = {
            'name': case_name,
            'result': res.name,
            'duration_ms': duration,
            'timestamp': time.time()
        }

        if ai_review is not None:
            case_entry['ai_review'] = asdict(ai_review)
        else:
            case_entry['ai_review'] = None

        file_handle.write(json.dumps(case_entry) + '\n')
        file_handle.flush()



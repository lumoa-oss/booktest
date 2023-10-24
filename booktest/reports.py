import logging
import os
import json

from enum import Enum


#
# Test results and CLI user interaction
#


class TestResult(Enum):
    OK = 1
    FAIL = 2
    DIFF = 3


def test_result_to_exit_code(test_result):
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
    This class manages the saved case specific metrics/results
    """

    def __init__(self, cases):
        self.cases = cases

    def passed(self):
        return [i[0] for i in self.cases if i[1] == TestResult.OK]

    def failed(self):
        return [i[0] for i in self.cases if i[1] != TestResult.OK]

    @staticmethod
    def of_file(file_name):
        cases = []
        for j in read_lines(file_name):
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
                    logging.exception(f"parsing line {j} failed with {e}")

        return CaseReports(cases)

    @staticmethod
    def write_case(file_handle,
                   case_name,
                   res: TestResult,
                   duration):
        file_handle.write(
            f"{case_name}\t{res.name}\t{duration}\n")

    def to_file(self, file):
        with open(file, "w") as f:
            for i in self.cases:
                CaseReports.write_case(f,
                                       i[0],
                                       i[1],
                                       i[2])



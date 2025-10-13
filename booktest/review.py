import os.path as path
import os
import shutil

from booktest.reports import TestResult, TwoDimensionalTestResult, CaseReports, UserRequest, read_lines, Metrics
from booktest.naming import to_filesystem_path


#
# Report and review functionality
#


BOOK_TEST_PREFIX = "BOOKTEST_"


def run_tool(config, tool, args):
    """ Run a tool used in reviews """
    cmd = config.get(tool, None)
    if cmd is not None:
        return os.system(f"{cmd} {args}")
    else:
        print(f"{tool} is not defined.")
        print(f"please define it in .booktest file or as env variable " +
              f"{BOOK_TEST_PREFIX + tool.upper()}")
        return 1


def interact(exp_dir, out_dir, case_name, test_result, config):
    # Convert pytest-style name to filesystem path (:: → /)
    case_name_fs = to_filesystem_path(case_name)
    exp_file_name = os.path.join(exp_dir, case_name_fs + ".md")
    out_file_name = os.path.join(out_dir, case_name_fs + ".md")
    log_file_name = os.path.join(out_dir, case_name_fs + ".log")

    rv = test_result
    user_request = UserRequest.NONE
    done = False

    while not done:
        options = []
        if test_result != TestResult.FAIL:
            options.append("(a)ccept")

        options.extend([
            "(c)ontinue",
            "(q)uit",
            "(v)iew",
            "(l)ogs",
            "(d)iff",
            "fast (D)iff"
        ])
        prompt = \
            ", ".join(options[:len(options) - 1]) + \
            " or " + options[len(options) - 1]

        if not config.get("verbose", False):
            print("    ", end="")

        answer = input(prompt)
        if answer == "a" and test_result != TestResult.FAIL:
            user_request = UserRequest.FREEZE
            done = True
        elif answer == "c":
            done = True
        elif answer == "q":
            user_request = UserRequest.ABORT
            done = True
        elif answer == "v":
            if os.path.exists(exp_file_name):
                arg = f"{exp_file_name} {out_file_name}"
            else:
                arg = out_file_name
            run_tool(config, "md_viewer", arg)
        elif answer == "l":
            run_tool(config, "log_viewer", log_file_name)
        elif answer == "d":
            run_tool(config,
                     "diff_tool",
                     f"{exp_file_name} {out_file_name}")
        elif answer == "D":
            run_tool(config,
                     "fast_diff_tool",
                     f"{exp_file_name} {out_file_name}")
    return rv, user_request


def freeze_case(exp_dir,
                out_dir,
                case_name):
    # Convert pytest-style name to filesystem path (:: → /)
    case_name_fs = to_filesystem_path(case_name)
    exp_dir_name = os.path.join(exp_dir, case_name_fs)
    exp_file_name = os.path.join(exp_dir, case_name_fs + ".md")
    out_dir_name = os.path.join(out_dir, case_name_fs)
    out_file_name = os.path.join(out_dir, case_name_fs + ".md")

    # destroy old test related files
    if path.exists(exp_dir_name):
        shutil.rmtree(exp_dir_name)
    os.rename(out_file_name, exp_file_name)
    if path.exists(out_dir_name):
        os.rename(out_dir_name, exp_dir_name)


def case_review(exp_dir, out_dir, case_name, test_result, config):
    # Convert pytest-style name to filesystem path (:: → /)
    case_name_fs = to_filesystem_path(case_name)
    always_interactive = config.get("always_interactive", False)
    interactive = config.get("interactive", False)
    complete_snapshots = config.get("complete_snapshots", False)

    # Extract success status from two-dimensional results early for interaction check
    from booktest.reports import TwoDimensionalTestResult, SuccessState, SnapshotState
    if isinstance(test_result, TwoDimensionalTestResult):
        success_status = test_result.success
        snapshot_status = test_result.snapshotting
        is_ok = (success_status == SuccessState.OK)
    else:
        success_status = test_result
        snapshot_status = None
        is_ok = (test_result == TestResult.OK)

    # Skip interactive mode if test is OK and we're auto-freezing with -s
    will_auto_freeze = (is_ok and complete_snapshots and
                        snapshot_status is not None and
                        snapshot_status == SnapshotState.UPDATED)

    do_interact = always_interactive
    if not is_ok and not will_auto_freeze:
        do_interact = do_interact or interactive

    if do_interact:
        rv, interaction = \
            interact(exp_dir, out_dir, case_name, test_result, config)
    else:
        rv = test_result
        interaction = UserRequest.NONE

    auto_update = config.get("update", False)
    auto_freeze = config.get("accept", False)

    # Use the already extracted status from above (for consistency with rv which may have changed)
    if isinstance(rv, TwoDimensionalTestResult):
        rv_success = rv.success
        rv_snapshot = rv.snapshotting
        is_ok_after = (rv_success == SuccessState.OK)
        is_diff_after = (rv_success == SuccessState.DIFF)
    else:
        is_ok_after = (rv == TestResult.OK)
        is_diff_after = (rv == TestResult.DIFF)

    # Auto-freeze conditions:
    # 1. User explicitly requested freeze in interactive mode
    # 2. Test passed (OK) and auto_update is enabled
    # 3. Test differed (DIFF) and auto_freeze is enabled
    # 4. Test passed (OK) with complete_snapshots (-s) and snapshots were updated
    should_freeze = (
        interaction == UserRequest.FREEZE or
        (is_ok_after and auto_update) or
        (is_diff_after and auto_freeze) or
        will_auto_freeze
    )

    if should_freeze:
        freeze_case(exp_dir, out_dir, case_name)
        # If we froze, update the result to OK
        if isinstance(rv, TwoDimensionalTestResult):
            # Keep as two-dimensional but mark success as OK
            rv = TwoDimensionalTestResult(SuccessState.OK, rv.snapshotting)
        else:
            rv = TestResult.OK

    return rv, interaction


def start_report(printer):
    printer()
    printer("# test results:")
    printer()


def report_case_begin(printer,
                      case_name,
                      title,
                      verbose):
    if verbose:
        if title is None:
            title = "test"
        printer(f"{title} {case_name}")
        printer()
    else:
        printer(f"  {case_name} - ", end="")


def report_case_result(printer,
                       case_name,
                       result,
                       took_ms,
                       verbose):
    from booktest.colors import yellow, red, green

    if verbose:
        printer()
        printer(f"{case_name} ", end="")

    int_took_ms = int(took_ms)

    # Handle two-dimensional results if available
    if isinstance(result, TwoDimensionalTestResult):
        # Format snapshot status message based on both dimensions
        snapshot_msg = ""

        if result.snapshotting.name == "FAIL":
            # Snapshot system failure - couldn't load/generate snapshots
            snapshot_msg = " (snapshot failure)"
        elif result.snapshotting.name == "UPDATED":
            if result.success.name == "FAIL":
                # Test failed but snapshots were successfully captured/updated
                snapshot_msg = " (snapshots updated)"
            elif result.success.name == "DIFF":
                # Test output differs and snapshots changed
                snapshot_msg = " (snapshots updated)"
            else:
                # Test OK and snapshots updated
                snapshot_msg = " (snapshots updated)"

        if result.success.name == "OK":
            if verbose:
                printer(f"{green('OK')} {int_took_ms} ms.{snapshot_msg}")
            else:
                printer(f"{green(str(int_took_ms) + ' ms')}{snapshot_msg}")
        elif result.success.name == "DIFF":
            printer(f"{yellow('DIFF')} {int_took_ms} ms{snapshot_msg}")
        elif result.success.name == "FAIL":
            printer(f"{red('FAIL')} {int_took_ms} ms{snapshot_msg}")
    else:
        # Legacy single-dimensional result
        if result == TestResult.OK:
            if verbose:
                printer(f"{green('ok')} in {int_took_ms} ms.")
            else:
                printer(f"{green(str(int_took_ms) + ' ms')}")
        elif result == TestResult.DIFF:
            printer(f"{yellow('DIFFERED')} in {int_took_ms} ms")
        elif result == TestResult.FAIL:
            printer(f"{red('FAILED')} in {int_took_ms} ms")

def maybe_print_logs(printer, config, out_dir, case_name):
    # Convert pytest-style name to filesystem path (:: → /)
    case_name_fs = to_filesystem_path(case_name)
    verbose = config.get("verbose", False)
    print_logs = config.get("print_logs", False)

    if print_logs:
        if verbose:
            lines = read_lines(out_dir, case_name_fs + ".log")
            if len(lines) > 0:
                printer()
                printer(f"{case_name} logs:")
                printer()
                # report case logs
                for i in lines:
                    printer("  " + i)
        else:
            lines = read_lines(out_dir, case_name_fs + ".log")
            if len(lines) > 0:
                printer()
                for i in lines:
                    printer("    log: " + i)
                printer(f"  {case_name}..", end="")




def report_case(printer,
                exp_dir,
                out_dir,
                case_name,
                result,
                took_ms,
                config):
    # Convert pytest-style name to filesystem path (:: → /)
    case_name_fs = to_filesystem_path(case_name)
    verbose = config.get("verbose", False)
    report_case_begin(printer,
                      case_name,
                      None,
                      verbose)

    if verbose:
        # report case content
        for i in read_lines(out_dir, case_name_fs + ".txt"):
            printer(i)

    maybe_print_logs(printer, config, out_dir, case_name)

    report_case_result(printer,
                       case_name,
                       result,
                       took_ms,
                       verbose)

    rv, request = case_review(exp_dir,
                              out_dir,
                              case_name,
                              result,
                              config)
    if verbose:
        printer()

    return rv, request


def end_report(printer, failed, tests, took_ms):
    """
    Print end of test run summary.

    Args:
        printer: Function to print output
        failed: List of failed test names OR list of (name, result, duration) tuples
        tests: Total number of tests
        took_ms: Total time taken in milliseconds
    """
    from booktest.colors import yellow, red

    printer()
    if len(failed) > 0:
        # Check if failed contains detailed info (tuples) or just names (strings)
        has_details = len(failed) > 0 and isinstance(failed[0], tuple)

        # Count DIFFs and FAILs
        if has_details:
            diff_count = sum(1 for _, result, _ in failed if result == TestResult.DIFF)
            fail_count = sum(1 for _, result, _ in failed if result == TestResult.FAIL)
        else:
            diff_count = 0
            fail_count = len(failed)

        # Build summary message
        parts = []
        if diff_count > 0:
            parts.append(f"{diff_count} differed")
        if fail_count > 0:
            parts.append(f"{fail_count} failed")

        summary = " and ".join(parts) if parts else "failed"
        printer(f"{len(failed)}/{tests} test {summary} in {took_ms} ms:")
        printer()

        # Print each failed test with details
        for item in failed:
            if has_details:
                name, result, duration = item
                # Extract file path for clickable link
                # Format: test/foo_test.py::ClassName/test_method
                file_path = name.split("::")[0] if "::" in name else name

                # Add color and status
                if result == TestResult.DIFF:
                    status = yellow("DIFF")
                else:
                    status = red("FAIL")

                # Format: file_path (clickable) :: rest of test name - STATUS
                if "::" in name:
                    rest = name[len(file_path):]  # Keep the ::
                    printer(f"  {file_path}{rest} - {status}")
                else:
                    printer(f"  {file_path} - {status}")
            else:
                # Legacy format: just test name
                printer(f"  {item}")
    else:
        printer(f"{tests}/{tests} test "
                f"succeeded in {took_ms} ms")
    printer()


def create_index(dir, case_names):
    with open(path.join(dir, "index.md"), "w") as f:
        def write(msg):
            f.write(msg)

        write("# Books overview:\n")
        domain = []
        for name in case_names:
            names = name.split("/")

            name_domain = names[:(len(names) - 1)]
            leaf_name = names[len(names) - 1]

            if name_domain != domain:
                cut = 0
                while (cut < len(name_domain) and
                       cut < len(domain) and
                       name_domain[cut] == domain[cut]):
                    cut += 1

                write("\n")
                for i in range(cut, len(name_domain)):
                    write(("    " * i) + " * " + name_domain[i] + "\n")

                domain = name_domain

            write(("    " * len(domain)) + f" * [{leaf_name}]({name}.md)\n")

        write("\n")


def review(exp_dir,
           out_dir,
           config,
           passed,
           cases=None):
    metrics = Metrics.of_dir(out_dir)
    report_txt = os.path.join(out_dir, "cases.txt")
    case_reports = CaseReports.of_file(report_txt)

    # Filter out test cases that no longer exist in the test suite
    if cases is not None:
        cases_set = set(cases)
        case_reports.cases = [
            (case_name, result, duration)
            for (case_name, result, duration) in case_reports.cases
            if case_name in cases_set
        ]

    if passed is None:
        passed = case_reports.passed()

    cont = config.get("continue", False)
    fail_fast = config.get("fail_fast", False)

    reviews = []
    rv = 0

    start_report(print)
    tests = 0
    abort = False
    for (case_name, result, duration) in case_reports.cases:
        reviewed_result = result
        if not abort:
            if (cases is None or case_name in cases) and \
               (not cont or case_name not in passed):
                tests += 1

                reviewed_result, request = \
                    report_case(print,
                                exp_dir,
                                out_dir,
                                case_name,
                                result,
                                duration,
                                config)

                if request == UserRequest.ABORT or \
                   (fail_fast and reviewed_result != TestResult.OK):
                    abort = True

        if reviewed_result != TestResult.OK:
            rv = -1

        reviews.append((case_name,
                        reviewed_result,
                        duration))

    updated_case_reports = CaseReports(reviews)
    updated_case_reports.to_file(report_txt)

    end_report(print,
               updated_case_reports.failed_with_details(),
               len(updated_case_reports.cases),
               metrics.took_ms)

    return rv

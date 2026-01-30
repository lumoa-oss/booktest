import os.path as path
import os
import shutil
import difflib
from typing import Optional

from booktest.reporting.reports import TestResult, TwoDimensionalTestResult, CaseReports, UserRequest, read_lines, Metrics
from booktest.config.naming import to_filesystem_path


#
# Report and review functionality
#


BOOK_TEST_PREFIX = "BOOKTEST_"


def perform_ai_review(exp_file_name: str, out_file_name: str, case_name: str) -> Optional['AIReviewResult']:
    """
    Perform AI review of test differences.

    Args:
        exp_file_name: Path to expected output file
        out_file_name: Path to actual output file
        case_name: Test case name

    Returns:
        AIReviewResult or None if review fails
    """
    try:
        from booktest.llm.llm_review import LlmReview, AIReviewResult
        from booktest.llm.llm import get_llm

        # Read expected and actual outputs
        if not os.path.exists(exp_file_name):
            print("    Error: Expected output file not found")
            return None

        if not os.path.exists(out_file_name):
            print("    Error: Actual output file not found")
            return None

        with open(exp_file_name, 'r') as f:
            expected = f.read()

        with open(out_file_name, 'r') as f:
            actual = f.read()

        # Generate unified diff
        expected_lines = expected.splitlines(keepends=True)
        actual_lines = actual.splitlines(keepends=True)
        diff = ''.join(difflib.unified_diff(
            expected_lines,
            actual_lines,
            fromfile='expected',
            tofile='actual',
            lineterm=''
        ))

        print("    Analyzing differences with AI...")

        # Create a dummy test case run for LlmReview (we only need the LLM)
        # We'll call review_test_diff directly without needing a full TestCaseRun
        llm = get_llm()

        # Create a minimal LlmReview instance
        class MinimalTestCaseRun:
            pass

        review = LlmReview(MinimalTestCaseRun(), llm)

        # Perform the review
        result = review.review_test_diff(
            test_name=case_name,
            expected=expected,
            actual=actual,
            diff=diff
        )

        return result

    except ImportError:
        print("    Error: LLM not configured. Set OPENAI_API_KEY or configure another LLM provider.")
        return None
    except Exception as e:
        print(f"    Error performing AI review: {e}")
        return None


def print_ai_review_result(result: 'AIReviewResult', verbose: bool = False):
    """
    Print AI review result to console.

    Args:
        result: The AI review result to print
        verbose: Whether to print full details or summary
    """
    from booktest.reporting.colors import yellow, red, green, gray

    print()
    print(f"    AI Review (confidence: {result.confidence:.2f}):")

    # Color-code the category
    category_str = result.category_name()
    if result.category <= 2:  # FAIL or RECOMMEND FAIL
        category_colored = red(category_str)
    elif result.category == 3:  # UNSURE
        category_colored = yellow(category_str)
    else:  # RECOMMEND ACCEPT or ACCEPT
        category_colored = green(category_str)

    print(f"      Category: {category_colored}")
    print(f"      Summary: {result.summary}")

    if verbose or result.category <= 3:
        # Show details for failures, unsure cases, or in verbose mode
        print()
        print(f"      Rationale:")
        for line in result.rationale.split('\n'):
            print(f"        {line}")

        if result.issues:
            print()
            print(f"      Issues:")
            for issue in result.issues:
                print(f"        - {issue}")

        if result.suggestions:
            print()
            print(f"      Suggestions:")
            for suggestion in result.suggestions:
                print(f"        - {suggestion}")

    if result.flags_for_human:
        print()
        print(f"      {yellow('⚠ Flagged for human review')}")

    print()


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


def interact(exp_dir, out_dir, case_name, test_result, config,
             existing_ai_result=None):
    # Convert pytest-style name to filesystem path (:: → /)
    case_name_fs = to_filesystem_path(case_name)
    exp_file_name = os.path.join(exp_dir, case_name_fs + ".md")
    out_file_name = os.path.join(out_dir, case_name_fs + ".md")
    log_file_name = os.path.join(out_dir, case_name_fs + ".log")

    rv = test_result
    user_request = UserRequest.NONE
    done = False

    # Extract success status from two-dimensional results
    from booktest.reporting.reports import TwoDimensionalTestResult, SuccessState
    if isinstance(test_result, TwoDimensionalTestResult):
        is_failed = (test_result.success == SuccessState.FAIL)
        is_diff = (test_result.success == SuccessState.DIFF)
    else:
        is_failed = (test_result == TestResult.FAIL)
        is_diff = (test_result == TestResult.DIFF)

    # Check if AI review is available for DIFF tests (only if not already done)
    ai_review_available = is_diff and not is_failed and existing_ai_result is None

    while not done:
        options = []
        if not is_failed:
            options.append("(a)ccept")

        options.extend([
            "(c)ontinue",
            "(q)uit",
            "(v)iew",
            "(l)ogs",
            "(d)iff",
            "fast (D)iff"
        ])

        if ai_review_available:
            options.append("AI (R)eview")

        prompt = \
            ", ".join(options[:len(options) - 1]) + \
            " or " + options[len(options) - 1] + "? "

        if not config.get("verbose", False):
            print("    ", end="")

        answer = input(prompt)
        if answer == "a" and not is_failed:
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
        elif (answer == "r" or answer == "R") and ai_review_available:
            # Perform AI review
            ai_result = perform_ai_review(exp_file_name, out_file_name, case_name)
            if ai_result:
                print_ai_review_result(ai_result, config.get("verbose", False))

                # Handle based on category
                if ai_result.category == 1:  # FAIL - auto-reject
                    print(f"    AI category: FAIL (confidence: {ai_result.confidence:.2f})")
                    print("    Continuing without accepting...")
                    done = True
                elif ai_result.category == 5:  # ACCEPT - auto-accept
                    print(f"    AI category: ACCEPT (confidence: {ai_result.confidence:.2f})")
                    print("    Auto-accepting...")
                    user_request = UserRequest.FREEZE
                    done = True
                elif ai_result.category == 2:  # RECOMMEND FAIL
                    confirm = input("    AI recommends rejecting. Continue without accepting? (y/n): ")
                    if confirm.lower() == 'y':
                        done = True
                elif ai_result.category == 4:  # RECOMMEND ACCEPT
                    confirm = input("    AI recommends accepting. Accept? (y/n): ")
                    if confirm.lower() == 'y':
                        user_request = UserRequest.FREEZE
                        done = True
                # For category 3 (UNSURE), just return to prompt for user decision
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
    ai_review_enabled = config.get("ai_review", False)

    # Extract success status from two-dimensional results early for interaction check
    from booktest.reporting.reports import TwoDimensionalTestResult, SuccessState, SnapshotState
    if isinstance(test_result, TwoDimensionalTestResult):
        success_status = test_result.success
        snapshot_status = test_result.snapshotting
        is_ok = (success_status == SuccessState.OK)
        is_diff = (success_status == SuccessState.DIFF)
    else:
        success_status = test_result
        snapshot_status = None
        is_ok = (test_result == TestResult.OK)
        is_diff = (test_result == TestResult.DIFF)

    # Perform automatic AI review if enabled and test has differences
    ai_result = None

    if ai_review_enabled and is_diff and not is_ok:
        exp_file_name = os.path.join(exp_dir, case_name_fs + ".md")
        out_file_name = os.path.join(out_dir, case_name_fs + ".md")

        ai_result = perform_ai_review(exp_file_name, out_file_name, case_name)

        # ALWAYS print AI review result when in interactive mode or verbose
        if ai_result:
            print_ai_review_result(ai_result, config.get("verbose", False))

    # Skip interactive mode if test is OK and we're auto-freezing with -s
    will_auto_freeze = (is_ok and complete_snapshots and
                        snapshot_status is not None and
                        snapshot_status == SnapshotState.UPDATED)

    # Skip interactive mode if AI gives definitive FAIL (1) or ACCEPT (5), unless forced with -I
    skip_interactive_due_to_ai = False
    if ai_result and ai_review_enabled and not always_interactive:
        if ai_result.should_skip_interactive():
            skip_interactive_due_to_ai = True
            if ai_result.category == 1:  # FAIL
                print(f"    AI category: FAIL (confidence: {ai_result.confidence:.2f})")
                print(f"    Skipping interactive mode (use -I to force interaction)")
            elif ai_result.category == 5:  # ACCEPT
                print(f"    AI category: ACCEPT (confidence: {ai_result.confidence:.2f})")
                print(f"    Skipping interactive mode (use -I to force interaction)")

    do_interact = always_interactive
    if not is_ok and not will_auto_freeze and not skip_interactive_due_to_ai:
        do_interact = do_interact or interactive

    if do_interact:
        # Pass AI result to interact function
        rv, interaction = \
            interact(exp_dir, out_dir, case_name, test_result, config, ai_result)
    else:
        rv = test_result
        interaction = UserRequest.NONE

        # In non-interactive mode or AI-skipped mode, check AI recommendation
        if ai_result and ai_review_enabled:
            if ai_result.should_auto_accept():
                interaction = UserRequest.FREEZE
            elif ai_result.should_auto_reject():
                # Keep as DIFF/FAIL, don't change rv
                pass

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

    return rv, interaction, ai_result


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
                       verbose,
                       out_dir=None,
                       case_reports=None):
    from booktest.reporting.colors import yellow, red, green, gray

    if verbose:
        printer()
        printer(f"{case_name} ", end="")

    int_took_ms = int(took_ms)

    # Check for AI review result if available
    ai_summary = ""
    ai_result = None

    # Get AI review from case_reports (stored in cases.ndjson)
    if case_reports is not None:
        ai_result = case_reports.get_ai_review(case_name)
        if ai_result is not None:
            ai_summary = f" ({gray('AI: ' + ai_result.summary)})"
    # Note: We no longer fall back to .ai.json files since AI reviews are now
    # stored in cases.ndjson and properly invalidated on test reruns

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
                printer(f"{green('ok')} {int_took_ms} ms.{snapshot_msg}{ai_summary}")
            else:
                printer(f"{green(str(int_took_ms) + ' ms')}{snapshot_msg}{ai_summary}")
        elif result.success.name == "DIFF":
            printer(f"{yellow('DIFF')} {int_took_ms} ms{snapshot_msg}{ai_summary}")
        elif result.success.name == "FAIL":
            printer(f"{red('FAIL')} {int_took_ms} ms{snapshot_msg}{ai_summary}")
    else:
        # Legacy single-dimensional result
        if result == TestResult.OK:
            if verbose:
                printer(f"{green('ok')} in {int_took_ms} ms.{ai_summary}")
            else:
                printer(f"{green(str(int_took_ms) + ' ms')}{ai_summary}")
        elif result == TestResult.DIFF:
            printer(f"{yellow('DIFFERED')} in {int_took_ms} ms{ai_summary}")
        elif result == TestResult.FAIL:
            printer(f"{red('FAILED')} in {int_took_ms} ms{ai_summary}")

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
                       verbose,
                       out_dir)

    rv, request, ai_result = case_review(exp_dir,
                                          out_dir,
                                          case_name,
                                          result,
                                          config)
    if verbose:
        printer()

    return rv, request, ai_result


def end_report(printer, failed, tests, took_ms):
    """
    Print end of test run summary.

    Args:
        printer: Function to print output
        failed: List of failed test names OR list of (name, result, duration) tuples
        tests: Total number of tests
        took_ms: Total time taken in milliseconds
    """
    from booktest.reporting.colors import yellow, red

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
    case_reports = CaseReports.of_dir(out_dir)

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

                reviewed_result, request, ai_result = \
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
    # Write updated reports back to cases.ndjson
    report_jsonl = os.path.join(out_dir, "cases.ndjson")
    with open(report_jsonl, 'w') as f:
        for case_name, result, duration in updated_case_reports.cases:
            # Preserve AI reviews if they exist
            ai_review = case_reports.get_ai_review(case_name)
            CaseReports.write_case_jsonl(f, case_name, result, duration, ai_review)

    # Don't show end_report summary in interactive mode
    # (user already reviewed failures interactively)
    if not config.get("interactive", False):
        end_report(print,
                   updated_case_reports.failed_with_details(),
                   len(updated_case_reports.cases),
                   metrics.took_ms)

    return rv

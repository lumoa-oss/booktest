import os.path as path
import os
import shutil

from booktest.reports import TestResult, CaseReports, UserRequest, read_lines, Metrics


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
    exp_file_name = os.path.join(exp_dir, case_name + ".md")
    out_file_name = os.path.join(out_dir, case_name + ".md")
    log_file_name = os.path.join(out_dir, case_name + ".log")

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
    exp_dir_name = os.path.join(exp_dir, case_name)
    exp_file_name = os.path.join(exp_dir, case_name + ".md")
    out_dir_name = os.path.join(out_dir, case_name)
    out_file_name = os.path.join(out_dir, case_name + ".md")

    # destroy old test related files
    if path.exists(exp_dir_name):
        shutil.rmtree(exp_dir_name)
    os.rename(out_file_name, exp_file_name)
    if path.exists(out_dir_name):
        os.rename(out_dir_name, exp_dir_name)


def case_review(exp_dir, out_dir, case_name, test_result, config):
    always_interactive = config.get("always_interactive", False)
    interactive = config.get("interactive", False)

    do_interact = always_interactive
    if test_result != TestResult.OK:
        do_interact = do_interact or interactive

    if do_interact:
        rv, interaction = \
            interact(exp_dir, out_dir, case_name, test_result, config)
    else:
        rv = test_result
        interaction = UserRequest.NONE

    auto_update = config.get("update", False)
    auto_freeze = config.get("accept", False)

    if (interaction == UserRequest.FREEZE or
       (rv == TestResult.OK and auto_update) or
       (rv == TestResult.DIFF and auto_freeze)):
        freeze_case(exp_dir, out_dir, case_name)
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
        printer(f"{title} {case_name}...")
        printer()
    else:
        printer(f"  {case_name}..", end="")


def report_case_result(printer,
                       case_name,
                       result,
                       took_ms,
                       verbose):
    if verbose:
        printer()
        printer(f"{case_name} ", end="")

    int_took_ms = int(took_ms)

    if result == TestResult.OK:
        if verbose:
            printer(f"ok in {int_took_ms} ms.")
        else:
            printer(f"{int_took_ms} ms")
    elif result == TestResult.DIFF:
        printer(f"DIFFERED in {int_took_ms} ms")
    elif result == TestResult.FAIL:
        printer(f"FAILED in {int_took_ms} ms")

def maybe_print_logs(printer, config, out_dir, case_name):
    verbose = config.get("verbose", False)
    print_logs = config.get("print_logs", False)

    if print_logs:
        if verbose:
            lines = read_lines(out_dir, case_name + ".log")
            if len(lines) > 0:
                printer()
                printer(f"{case_name} logs:")
                printer()
                # report case logs
                for i in lines:
                    printer("  " + i)
        else:
            lines = read_lines(out_dir, case_name + ".log")
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
    verbose = config.get("verbose", False)
    report_case_begin(printer,
                      case_name,
                      None,
                      verbose)

    if verbose:
        # report case content
        for i in read_lines(out_dir, case_name + ".txt"):
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
    printer()
    if len(failed) > 0:
        printer(f"{len(failed)}/{tests} test "
                f"failed in {took_ms} ms:")
        printer()
        for f in failed:
            printer(f"  {f}")
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
               updated_case_reports.failed(),
               len(updated_case_reports.cases),
               metrics.took_ms)

    return rv

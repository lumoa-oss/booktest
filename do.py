"""./do script is used to run lint, test and various scripts."""
import argparse
import sys
import os
import cProfile
from coverage import Coverage
import argcomplete

import test.tests as tst

TEST_ROOT_DIR = "books"


MIN_COVERAGE_PERCENT = 25


def coverage(parsed) -> int:

    args = parsed.args

    if len(args) == 0:
        args = ["test", "-p"]

    # remove old main coverage and process coverage files
    if os.path.exists(".coverage"):
        os.remove(".coverage")
    for i in os.listdir("."):
        if i.startswith(".coverage."):
            os.remove(i)

    cov = Coverage()
    cov.start()

    do_args(args)

    cov.stop()
    cov.save()
    cov.combine()

    percent = cov.report()

    cov.xml_report(outfile="coverage.xml")

    print()
    print(f"coverage: {percent:.1f}% / {MIN_COVERAGE_PERCENT}%")
    print()

    if percent >= MIN_COVERAGE_PERCENT:
        return 0
    else:
        return -1


def lint():
    rv = os.system('pycodestyle do.py `find booktest test -name "*.py" `')
    if rv == 0:
        return 0
    else:
        return -1


def test(args, cache={}):
    return tst.tests.exec(TEST_ROOT_DIR, args, cache)


def qa() -> int:
    print("# running lint...")
    if lint() == 0:
        print("ok")
        return test(["-f"])
    else:
        return -1


def autocomplete_script() -> int:
    print('eval "$(register-python-argcomplete do)"')
    return 0


def deploy() -> int:
    return os.system("python setup.py sdist upload -r local")


def sdist() -> int:
    return os.system("python setup.py sdist")


def install() -> int:
    return os.system("python setup.py install")


def uninstall() -> int:
    return os.system("pip uninstall booktest")


def clean() -> int:
    return os.system("rm -r build dist booktest.egg-info")


def do(cmd, cache=None):
    if cache is None:
        cache = {}
    do_args(cmd.split(" "), cache)


def setup_subparser(subparsers):
    profile_parser = \
        subparsers.add_parser('profile',
                              help='runs the remaining command in profiler')
    profile_parser.add_argument("args", nargs='*')
    profile_parser.set_defaults(
        exec=lambda parsed:
            cProfile.run(f"do_args({parsed.args})")
    )

    qa_parser = subparsers.add_parser('qa',
                                      help='runs linter and test')
    qa_parser.set_defaults(
        exec=lambda parsed: qa())

    subparsers\
        .add_parser(
            'autocomplete-script',
            help='enables autocomplete with ' +
                 '\'eval "$(./do autocomplete-script)\'') \
        .set_defaults(
            exec=lambda parsed: autocomplete_script())

    coverage_parser = \
        subparsers.add_parser('coverage',
                              help='runs the remaining command in coverage.py')
    coverage_parser.add_argument("args", nargs='*')
    coverage_parser.set_defaults(exec=coverage)

    subparsers\
        .add_parser('lint',
                    help='runs linter') \
        .set_defaults(
            exec=lambda parsed: lint())


def do_args(args, cache={}) -> int:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='sub-command help')

    setup_subparser(subparsers)

    tests_parser = subparsers.add_parser("test")
    tst.tests.setup_parser(tests_parser)
    tests_parser.set_defaults(
        exec=lambda parsed:
            tst.tests.exec_parsed(TEST_ROOT_DIR,
                                  parsed,
                                  cache))

    argcomplete.autocomplete(parser)
    parsed = parser.parse_args(args)

    return parsed.exec(parsed)


if __name__ == "__main__":
    ev = do_args(sys.argv[1:], {})
    if ev != 0:
        exit(ev)

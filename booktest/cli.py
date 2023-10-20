"""
This package introduces the lumoa-rl cli interface.
It can be used for creating insights or for creating topics.
"""

import argparse
import argcomplete

import sys

import booktest as bt
from booktest.config import get_default_config
from booktest.detection import detect_tests


def add_exec(parser, method):
    parser.set_defaults(
        exec=method)


config_comments = {
    "diff_tool":
"""#
# diff_tool is used to see changes in the results
#
# one option is Meld: https://meldmerge.org/
#
# install in Debian based distros with
#   'sudo apt install meld'
#
""",
    "md_viewer":
"""#
# md_viewer is used to view the md content, like tables, lists, links and images
#
# one option is retext, which is an md editor
#
# Retext - https://github.com/retext-project/retext
#
""",
    "test_paths":
"""#
# default paths for looking up test cases
#
""",
    "default_tests":
"""#
# default tests to run, when no argument given
#
""",
    "books_path":
"""#
# default location for storing the results and books
#
"""
}

config_defaults = {
    "diff_tool": "meld",
    "md_viewer": "retext --preview",
    "test_paths": "test,book,run",
    "default_tests": "test,book",
    "books_path": "books"
}


def prompt_config(prompt,
                  key,
                  config):
    default_value = config.get(key)
    if default_value is None:
        default_value = config_defaults.get(key)
    value = input(f"{prompt} (default '{default_value}'):")
    if not value:
        value = default_value
    return key, value


def setup_booktest(parsed):
    config = get_default_config()

    configs = []
    configs.append(prompt_config("specify diff tool", "diff_tool", config))
    configs.append(prompt_config("specify md viewer", "md_viewer", config))
    configs.append(prompt_config("specify all test paths", "test_paths", config))
    configs.append(prompt_config("specify default test paths", "default_tests", config))
    configs.append(prompt_config("specify directory for storing books", "books_path", config))

    with open(".booktest", "w") as f:
        for key, value in configs:
            f.write(config_comments[key])
            f.write(f"{key}={value}\n\n")
    print("updated .booktest")


def setup_test_suite(parser):
    config = get_default_config()

    default_paths = config.get("test_paths", "test,book,run").split(",")

    tests = []
    for path in default_paths:
        tests.extend(detect_tests(path, include_in_sys_path=True))

    test_suite = bt.merge_tests(tests)
    test_suite.setup_parser(parser)
    books_dir = config.get("books_path", "books")
    parser.set_defaults(
        exec=lambda args: test_suite.exec_parsed(books_dir, args))

    subparsers = parser.add_subparsers(help='sub-command help')

    setup_parser = \
        subparsers.add_parser('setup',
                              help='sets up the booktest')
    setup_parser.set_defaults(
        exec=lambda parsed: setup_booktest(parsed))


def exec_parsed(parsed):
    return parsed.exec(parsed)


def main(arguments=None):
    parser = argparse.ArgumentParser(description='booktest - review driven test tool')

    setup_test_suite(parser)
    argcomplete.autocomplete(parser)

    args = parser.parse_args(args=arguments)

    if "exec" in args:
        exec_parsed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main(sys.argv)

from booktest.config import get_default_config, DEFAULT_TIMEOUT
import os


personal_comment = \
"""
#
# This file is meant for personal UI configuration with booktest 
#
# This file should be included in .gitignore and never commited to version control!
#
"""

project_comment = \
"""
#
# This file is meant for project specific configuration like python paths and test file location
#
# This file should be included in the version control.
#
"""


config_comments = {
    "diff_tool":
"""#
# diff_tool is the tool used to see changes in the results
#
# one option is Meld: https://meldmerge.org/
#
# you can install 'meld' in Debian based distros with
#
#   'sudo apt install meld'
#
""",
    "fast_diff_tool":
"""#
#
# fast_diff_tool is used to see changes in the results quickly
#
# default option is diff, which should be present in most systems
#
""",
    "md_viewer":
"""#
# md_viewer is the tool used to view the md content, like tables, lists, links and images
#
# one option is retext, which is an md editor
#
# Retext - https://github.com/retext-project/retext
#
# you can install 'retext' in Debian based distros with
#
#   'sudo apt install retext'
#
""",
    "log_viewer":
"""#
#
# log_viewer is used to view the logs
#
# one option is less, which should be present in most systems
#
""",
    "python_path":
"""#
# the python_path is used to specify the directories where the python modules are located
#
# by default, it is 'src:.', which means that the src directory and the current directory are searched
#
""",
    "test_paths":
"""#
# booktest automatically detects tests in the default_tests directories
#
""",
    "default_tests":
"""#
# booktest will run all default_tests test cases, if no argument is given
#
""",
    "books_path":
"""#
# books_path specifies directory, where results and books are stored
#
""",
    "timeout":
"""#
# timeout specifies the test timeout in seconds for parallel runs. 
#
"""

}

config_defaults = {
    "diff_tool": "meld",
    "fast_diff_tool": "diff",
    "md_viewer": "retext --preview",
    "log_viewer": "less",
    "python_path": "src:.",
    "test_paths": "test,book,run",
    "default_tests": "test,book",
    "books_path": "books",
    "timeout": DEFAULT_TIMEOUT
}


def prompt_config(key,
                  config):
    print(config_comments[key])

    default_value = config.get(key)
    if default_value is None:
        default_value = config_defaults.get(key)
    value = input(f"specify {key} (default '{default_value}'):")
    if not value:
        value = default_value

    print()
    print(f"{key}={value}")
    print()

    return key, value


def setup_personal():
    config = get_default_config()

    print()
    print("setup asks you to specify various tools and paths for your personal booktest config in ~/.booktest")
    print("==================================================================================================")
    print()

    configs = []
    configs.append(prompt_config("diff_tool", config))
    configs.append(prompt_config("fast_diff_tool", config))
    configs.append(prompt_config("md_viewer", config))
    configs.append(prompt_config("log_viewer", config))

    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, ".booktest")

    with open(file_path, "w") as f:
        f.write(personal_comment)
        f.write("\n")
        for key, value in configs:
            f.write(config_comments[key])
            f.write(f"{key}={value}\n\n")
    print(f"updated {file_path}")

    return 0


def setup_project():
    config = get_default_config()

    print()
    print("setup asks you to specify various tools and paths for booktest project config in booktest.ini")
    print("=============================================================================================")
    print()

    configs = []
    configs.append(prompt_config("python_path", config))
    configs.append(prompt_config("test_paths", config))
    configs.append(prompt_config("default_tests", config))
    configs.append(prompt_config("books_path", config))
    configs.append(prompt_config("timeout", config))

    with open("booktest.ini", "w") as f:
        f.write(project_comment)
        f.write("\n")
        for key, value in configs:
            f.write(config_comments[key])
            f.write(f"{key}={value}\n\n")
    print("updated booktest.ini")

    return 0

def setup_booktest():
    setup_project()
    setup_personal()

    return 0

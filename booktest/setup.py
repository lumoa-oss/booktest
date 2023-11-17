from booktest.config import get_default_config


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
"""
}

config_defaults = {
    "diff_tool": "meld",
    "md_viewer": "retext --preview",
    "test_paths": "test,book,run",
    "default_tests": "test,book",
    "books_path": "books"
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


def setup_booktest():
    config = get_default_config()

    print()
    print("setup asks you to specify various tools and paths for booktest")
    print("==============================================================")
    print()

    configs = []
    configs.append(prompt_config("diff_tool", config))
    configs.append(prompt_config("md_viewer", config))
    configs.append(prompt_config("test_paths", config))
    configs.append(prompt_config("default_tests", config))
    configs.append(prompt_config("books_path", config))

    with open(".booktest", "w") as f:
        for key, value in configs:
            f.write(config_comments[key])
            f.write(f"{key}={value}\n\n")
    print("updated .booktest")

    return 0

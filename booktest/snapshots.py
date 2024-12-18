from booktest import TestCaseRun

import os


def out_snapshot_path(t: TestCaseRun, path: str):
    # in the new version, let's still keep the dot prefix to avoid name conflicts, but
    # keep everything inside .snapshots folder to avoid conflicts with .gitignore
    return t.file(os.path.join(".snapshots", path))


def frozen_snapshot_path(t: TestCaseRun, path: str):
    # old path for legacy compatibility
    #
    # the problem with old snapshot paths was that e.g. '.env.json' would
    # end up in .gitignore, which was a major issue
    #
    rv = os.path.join(t.exp_dir_name, "." + path)
    if os.path.exists(rv):
        return rv

    # new path
    rv = os.path.join(t.exp_dir_name, ".snapshots", path)
    return rv


def have_snapshots_dir(t):
    os.makedirs(t.file(".snapshots"), exist_ok=True)


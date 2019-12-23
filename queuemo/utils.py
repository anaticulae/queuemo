# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here"""

import os
import subprocess
from subprocess import PIPE
from subprocess import CompletedProcess

from utila import info


def run(command: str, cwd: str = None, env: dict = None) -> CompletedProcess:
    """Run external process

    Args:
        command(str/[str]): command to run
        cwd(str): current working directory
        env(dict): modify environment variable for test run. If nothing is
                   passed, the global environment variable is used.
    Returns:
        return completed process
    """
    cwd = cwd if cwd else os.getcwd()
    assert os.path.exists(cwd)
    msg = 'cwd %s is not a valid directory' % cwd
    assert os.path.isdir(cwd), msg

    env = os.environ if env is None else env
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        errors='replace',
        shell=True,
        stderr=PIPE,
        stdout=PIPE,
        universal_newlines=True,
    )
    return completed


def print_env():
    """Print environment vars if logging level is higher, equal than
    INFORMATION.

    TODO: MOVE TO UTILA
    """
    for key, value in os.environ.items():
        info('{:<40}{}'.format(key, value))

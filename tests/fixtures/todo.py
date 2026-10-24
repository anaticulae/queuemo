# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import utilo

import queuemo
import queuemo.runtime.runtime
import tests


@contextlib.contextmanager
def runtime(
    workspace,
    document: str,
    recipes: list | tuple,
    mp,
    config=None,
) -> queuemo.runtime.runtime.RecipeRuntime:
    workspace = str(workspace)
    if not utilo.iterable(recipes):
        recipes = [recipes]
    with tests.patch_todo(workspace, mp, copy=True):
        # Hint: do not use link, cause multiprocessed tests modify global
        # variables.
        # outpath = qvlink.todo(document)
        outpath = os.path.join(workspace, 'todo_', document)
        current = queuemo.runtime.runtime.RecipeRuntime(
            workspace=workspace,
            document=document,
            outpath=outpath,
            config=config,
        )
        for item in recipes:
            current.append(item)
        yield current

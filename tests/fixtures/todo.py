# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import queuemo
import queuemo.runtime.runtime
import tests
import tests.resources


@contextlib.contextmanager
def runtime(
    workspace,
    document,
    recipes,
    monkeypatch,
    config=None,
) -> queuemo.runtime.runtime.RecipeRuntime:
    workspace = str(workspace)

    if not isinstance(recipes, list):
        recipes = [recipes]

    with tests.patch_todo(workspace, monkeypatch, copy=True):
        # Hint: do not use link, cause multiprocessed tests modify global
        # variables.
        # outpath = link.todo(document)
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

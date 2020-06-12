# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import link

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
) -> queuemo.runtime.runtime.RecipeRuntime:
    workspace = str(workspace)

    if not isinstance(recipes, list):
        recipes = [recipes]

    with tests.patch_todo(workspace, monkeypatch, copy=True):
        outpath = link.todo(document)
        current = queuemo.runtime.runtime.RecipeRuntime(
            workspace=workspace,
            document=document,
            outpath=outpath,
        )
        for item in recipes:
            current.append(item)
        yield current

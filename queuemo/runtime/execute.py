# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link

import queuemo.recipes
import queuemo.runtime.runtime


def run_document(workspace: str, document: str, outpath: str):
    # queuemo.runnable.check(RUNNER)

    runtime = queuemo.runtime.runtime.RecipeRuntime(
        workspace=workspace,
        document=document,
        outpath=outpath,
    )

    for item in queuemo.recipes.ORDER:
        runtime.append(item)
    maxsteps = len(runtime)

    while True:
        current = runtime.next_step()
        link.update_progress_step(
            document,
            value=maxsteps - len(runtime),
            maxvalue=maxsteps,
        )
        if current is None:
            # Done, everthing completed successful.
            break
        if not current:
            # Failure
            link.fail(document)
            break

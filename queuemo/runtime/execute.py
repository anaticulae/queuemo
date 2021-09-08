# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link

import queuemo.recipes
import queuemo.recipes.logger
import queuemo.runtime.api
import queuemo.runtime.runtime


def run_document(
    workspace: str,
    documentid: str,
    outpath: str,
    config=None,
):
    if config is None:
        config = queuemo.runtime.api.RecipeConfig()
    # queuemo.runnable.check(RUNNER)
    runtime = queuemo.runtime.runtime.RecipeRuntime(
        workspace=workspace,
        document=documentid,
        outpath=outpath,
        config=config,
    )

    for item in queuemo.recipes.ORDER:
        runtime.append(item)
    # TODO: INVESTIGATE ABOUT 3
    maxsteps = sum(len(step) for step in runtime) + 3

    def tick():
        link.update_progress_step(
            documentid,
            value=tick.number,
            maxvalue=maxsteps,
        )
        tick.number += 1

    tick.number = 0
    while True:
        current = runtime.next_step(tick)
        if current is None:
            # Done, everything completed successfully.
            break
        if not current:
            # Failure
            if not link.failed(documentid):
                # already failed cause of unsupported document. check
                # before to avoid overwriting error message
                error = queuemo.recipes.logger.content()
                link.fail(documentid, error=error)
            break

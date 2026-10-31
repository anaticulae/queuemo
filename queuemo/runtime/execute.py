# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import qvlink
import utilo

import queuemo.recipes
import queuemo.recipes.logger
import queuemo.runtime.api
import queuemo.runtime.runtime


def run_document(
    workspace: str,
    documentid: str,
    outpath: str,
    config=None,
) -> int:
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
        qvlink.update_progress_step(
            documentid,
            value=tick.number,
            maxvalue=maxsteps,
        )
        tick.number += 1

    tick.number = 0
    while True:  # pylint:disable=W0149
        current = runtime.next_step(tick)
        if current is None:
            # Done, everything completed successfully.
            break
        if not current:
            # Failure
            if not qvlink.failed(documentid):
                # already failed cause of unsupported document. check
                # before to avoid overwriting error message
                error = queuemo.recipes.logger.content()
                qvlink.fail(documentid, error=error)
                return utilo.FAILURE
            break
    return utilo.SUCCESS

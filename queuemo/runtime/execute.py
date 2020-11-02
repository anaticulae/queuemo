# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

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

    while True:
        current = runtime.next_step()
        if current is None:
            # Done, everthing completed successful.
            break
        if not current:
            # Failure
            break

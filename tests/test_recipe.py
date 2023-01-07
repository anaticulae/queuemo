# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilatest

import queuemo.runtime
import queuemo.runtime.api
import queuemo.runtime.execute
import queuemo.worker.startup
import tests
import tests.resources


@utilatest.nightly
def test_recipe_run(td, mp):
    root = str(td)
    with tests.patch_todo(td, mp):
        workspace = queuemo.worker.startup.copy(tests.resources.EXAMPLE_JOB)
        queuemo.runtime.execute.run_document(
            workspace,
            documentid=tests.resources.EXAMPLE_JOB,
            outpath=root,
        )
    # TODO: VERIFY RESULT WITH ASSERTION

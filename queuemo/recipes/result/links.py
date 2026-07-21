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

import queuemo.runnable
import queuemo.runtime.api


def run(flow: queuemo.runtime.api.RecipeIO):
    if flow.skip(queuemo.runnable.decider_links):
        return
    queuemo.runnable.words_links(
        inpath=flow.general,
        outpath=flow.tmppath,
    )
    queuemo.runnable.decider_links(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()

    resultview = qvlink.resultview(flow.document)
    utilo.copy_content(
        flow.general,
        resultview,
        pattern='words__links_links.yaml',
        verbose=True,
    )

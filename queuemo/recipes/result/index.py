# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Index
=====
"""

import iamraw
import utila

import queuemo.runnable
import queuemo.runtime.api
import queuemo.utils


def run(flow: queuemo.runtime.api.RecipeIO):  # pylint:disable=W0613
    pass


def run_detector_index(flow: queuemo.runtime.api.RecipeIO):
    indexpages = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.Index,
    )
    if indexpages == ':':
        utila.debug('could not locate index page, skip detector --index')
        return
    queuemo.runnable.detector_index(
        flow.general,
        flow.tmppath,
        pages=indexpages,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()

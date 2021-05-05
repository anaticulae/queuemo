# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Title page fast view
====================

requirements:

* rawmaker --oneline

steps
-----

run
~~~

1. Run dectector with --titlepage to extract elements on titlepage
2. Run decider --titlepage to judge extracted elements and mark missing
   elements

after
~~~~~

publish linter result

"""

import iamraw.sections
import utila

import queuemo.runnable
import queuemo.runtime.api
import queuemo.utils


def run(flow: queuemo.runtime.api.RecipeIO):
    decide_title(flow)
    decide_toc(flow)


def decide_title(flow: queuemo.runtime.api.RecipeIO):
    titlepage = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.TitlePage,
    )
    queuemo.runnable.detector_titlepage(
        flow.general,
        flow.tmppath,
        pages=titlepage,
    )
    queuemo.runnable.decider_titlepage(flow.tmppath, flow.tmppath)


def decide_toc(flow: queuemo.runtime.api.RecipeIO):
    sources = [flow.general, flow.tmppath]
    if not queuemo.utils.exists('groupme__toc_toc.yaml', sources):
        utila.error('could not locate groupme__toc_toc.yaml, skip decider_toc')
        return
    queuemo.runnable.decider_toc(
        inpath=sources,
        output=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()

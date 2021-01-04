# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

import queuemo.runnable
import queuemo.runtime.api
import queuemo.utils

PREFIX = '01'


def run(flow: queuemo.runtime.api.RecipeIO):
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


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()

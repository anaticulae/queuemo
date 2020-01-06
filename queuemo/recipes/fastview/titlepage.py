# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
import queuemo.recipe
import queuemo.recipes.api

PREFIX = '01'


def run(flow: queuemo.recipes.api.RecipeIO):
    queuemo.recipes.detector_titlepage(flow.general, flow.tmppath)
    queuemo.recipes.decider_titlepage(flow.tmppath, flow.tmppath)


def after(flow: queuemo.recipes.api.RecipeIO):
    flow.publish_linting()

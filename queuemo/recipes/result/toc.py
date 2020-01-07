# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import queuemo.recipes
import queuemo.recipes.api


def run(flow: queuemo.recipes.api.RecipeIO):
    queuemo.recipes.groupme(flow.general, flow.tmppath)
    queuemo.recipes.decider_toc(flow.tmppath, flow.tmppath)

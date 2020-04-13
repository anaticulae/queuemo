# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import queuemo.recipes
import queuemo.runnable
import queuemo.runtime.api


def before(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.groupme(
        inpath=[
            flow.general,
        ],
        output=flow.general,
    )
    queuemo.runnable.decider_border_detecion(
        inpath=[
            flow.general,
        ],
        output=flow.tmppath,
    )
    queuemo.runnable.decider_border_distance(
        inpath=[
            flow.general,
        ],
        output=flow.tmppath,
    )
    flow.publish_linting(fastview=False)


def run(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.feedback_images(
        inpath=[
            flow.general,
        ],
        output=flow.tmppath,
    )
    queuemo.runnable.feedback_view(
        inpath=[
            flow.general,
            flow.tmppath,
        ],
        output=flow.tmppath,
    )
    # TODO: Support utila to create result without package feedback
    # For example generate: 0.html, 1.html etc. nor package_0.html,
    # package_1.html
    flow.publish(folder='feedback__view_pages', pattern='*.html')
    flow.publish(folder='feedback__view_pages', pattern='*.jpg')
    flow.publish(folder='feedback__view_pages', pattern='*.png')

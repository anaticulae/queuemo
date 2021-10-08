# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import utila

import queuemo.runnable
import queuemo.runtime.api


@queuemo.required
def before(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.decider_border_detecion(
        inpath=[
            flow.general,
        ],
        outpath=flow.tmppath,
    )
    queuemo.runnable.decider_border_distance(
        inpath=[
            flow.general,
        ],
        outpath=flow.tmppath,
    )
    flow.publish_linting()
    # optimize findings
    active = None
    if flow.config and flow.config.webconfig:
        # do not publish all findings, publish just select onces
        active = flow.config.webconfig.active
    link.write_optimized_findings(
        document=flow.document,
        active=active,
    )


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.feedback_images(
        inpath=flow.general,
        outpath=flow.tmppath,
    )
    queuemo.runnable.feedback_view(
        inpath=[
            link.resultview(flow.document),
            flow.general,
            flow.tmppath,
        ],
        outpath=flow.tmppath,
    )


def run_plot(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.feedback_plot(
        inpath=[
            link.resultview(flow.document),
            flow.general,
            flow.tmppath,  # TODO: WHICH IS CORRECT PATH
        ],
        outpath=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    # TODO: Support utila to create result without package feedback
    # For example generate: 0.html, 1.html etc. nor package_0.html,
    # package_1.html
    flow.publish(folder='feedback__view_pages', pattern='*.html')
    flow.publish(folder='feedback__view_pages', pattern='*.jpg')
    flow.publish(folder='feedback__view_pages', pattern='*.png')

    resultview = link.resultview(flow.document)
    utila.copy_content(
        flow.tmppath,
        os.path.join(resultview, 'view'),
        pattern='feedback__plot_*.png',
        verbose=True,
    )

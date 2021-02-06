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
        output=flow.tmppath,
    )
    queuemo.runnable.decider_border_distance(
        inpath=[
            flow.general,
        ],
        output=flow.tmppath,
    )
    flow.publish_linting()


@queuemo.required
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
        ] + findings(flow),
        output=flow.tmppath,
    )
    queuemo.runnable.feedback_plot(
        inpath=[
            flow.general,
            flow.tmppath,  # TODO: WHICH IS CORRECT PATH
        ] + findings(flow),
        output=flow.tmppath,
    )


def findings(flow) -> list:
    result = [
        flow.package('bibliography'),
        flow.package('chapter'),
        flow.package('doctextstyle'),
        flow.package('footnote'),
        flow.package('imgfig'),
        flow.package('intro'),
        flow.package('links'),
        flow.package('magic'),
        flow.package('smarty'),
        flow.package('textflow'),
    ]
    return result


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
        pattern='feedback__plot_findings_histogram.png',
        verbose=True,
    )

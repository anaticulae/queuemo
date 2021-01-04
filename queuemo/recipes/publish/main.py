# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import utila

import queuemo
import queuemo.runtime.api


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO):
    # copy todo folder to result and create done folder
    link.publish(flow.document)


@queuemo.required
def after(flow: queuemo.runtime.api.RecipeIO):
    utila.log(f'publish log')
    ready = link.ready(flow.document)

    if utila.logger.OUTFILE:
        utila.copy_content(
            utila.logger.OUTFILE,
            ready,
            verbose=True,
        )
    else:
        utila.error('no utila.logger.OUTFILE defined, could not publish')

    # document completed
    utila.log()
    utila.log((('#' * 80) + utila.NEWLINE) * 4)
    utila.log()

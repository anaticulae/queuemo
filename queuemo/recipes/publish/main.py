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

import queuemo
import queuemo.runtime.api


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO):
    # copy todo folder to result and create done folder
    link.publish(flow.document)

    # TODO: MOVE TO LINK finish_resultview
    write_queuemo_version(flow.document)


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
        utila.error(('no utila.logger.OUTFILE defined,'
                     ' could not publish log file'))

    # document completed
    utila.log()
    utila.log((('#' * 80) + utila.NEWLINE) * 4)
    utila.log()


def write_queuemo_version(document: str):
    ready = link.ready(document)
    debug = os.path.join(ready, 'debug')
    # queuemo 1.8.0 to debug file
    utila.run(f'queuemo -v -V >> {debug}')

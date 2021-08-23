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
import queuemo.recipes.logger
import queuemo.runtime.api


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO):
    # copy todo folder to result and create done folder
    if link.todo(flow.document) != link.ready(flow.document):
        # if todo and ready is the same folder, publish is not necessary
        # anymore.
        link.publish(
            flow.document,
            skip_resultview=skip_resultview,
        )
    link.write_debug(flow.document, list=USED)
    link.publish_statistics(flow.document)


@queuemo.required
def after(flow: queuemo.runtime.api.RecipeIO):
    utila.log('publish log')
    ready = link.ready(flow.document)
    if utila.logger.OUTFILE:
        content = queuemo.recipes.logger.content()
        logpath = os.path.join(ready, 'done')
        # write current document log to result
        utila.log(f'write log to: {logpath}')
        utila.file_create(logpath, content)
    else:
        utila.error('no utila.logger.OUTFILE defined could not publish logfile')
    # document completed
    utila.log()
    utila.log((('#' * 80) + utila.NEWLINE) * 4)
    utila.log()


USED = utila.splitlines("""
caption
chapter
decider
decider_abbreviation
decider_bibliography
decider_border
decider_chapter
decider_chapter
decider_footnote
decider_imgfig
decider_smarty
decider_textstyle
decider_toc
detector
docref
docstyle
feedback
figureo
groupme
magic
queuemo
rawmaker
rawmaker_cleanup
sections
smarty
spacestation
tablero
textflow
words
""")


def skip_resultview(path) -> bool:
    path = str(path)
    if path.endswith('_user.yaml'):
        return True
    return False

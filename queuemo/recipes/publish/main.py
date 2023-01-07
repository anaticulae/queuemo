# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import utila

import queuemo
import queuemo.recipes.logger
import queuemo.runnable
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


def run_debug(flow: queuemo.runtime.api.RecipeIO):
    link.write_debug(
        flow.document,
        todo=queuemo.runnable.RUNNER,
        requirements=True,
    )


def run_statistics(flow: queuemo.runtime.api.RecipeIO):
    link.publish_statistics(flow.document)


@queuemo.required
def after(flow: queuemo.runtime.api.RecipeIO):
    utila.log('publish log')
    ready = link.ready(flow.document)
    if utila.outfile():
        content = queuemo.recipes.logger.content()
        logpath = os.path.join(ready, 'done')
        # write current document log to result
        utila.log(f'write log to: {logpath}')
        utila.file_replace(logpath, content)
    else:
        utila.error('no utila.outfile_setup defined could not publish logfile')
    # document completed
    utila.log()
    utila.log((('#' * 80) + utila.NEWLINE) * 4)
    utila.log()


def skip_resultview(path) -> bool:
    path = str(path)
    if path.endswith('_user.yaml'):
        return True
    return False

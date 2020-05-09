# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import concurrent
import functools

import link
import utila

import queuemo.runnable
import queuemo.runtime.api
import queuemo.runtime.runtime


def before(flow: queuemo.runtime.api.RecipeIO):
    if link.current(flow.document) == link.ProcessState.VERIFIED:
        # if fastview is not started before, start analysis with resultview
        link.start_analysis(flow.document)


def run(flow: queuemo.runtime.api.RecipeIO):
    pdf = flow.sourcepath

    todo = []
    todo.append(
        functools.partial(
            queuemo.runnable.rawmaker,
            inpath=pdf,
            outpath=flow.tmppath,
            text=True,
            font=True,
            border=True,
            boxes=True,
            images=True,
            line=True,
            outlines=True,
        ))
    todo.append(
        functools.partial(
            queuemo.runnable.rawmaker,
            inpath=pdf,
            outpath=flow.tmppath,
            prefix='oneline',
            boxes_flow=1.0,
            char_margin=100,
            line_margin=0.1,
            text=True,
        ))
    completed = run_parallel(*todo)

    # ensure rawmaker is completed before running linero
    completed = queuemo.runnable.linero(
        inpath=flow.tmppath,
        output=flow.tmppath,
    )
    assert completed == utila.SUCCESS, str(completed)
    return [completed]


def run_parallel(*items, worker=2) -> int:
    ret = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = {executor.submit(item): item for item in items}
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as error:  # pylint:disable=broad-except
                utila.error(f'{future} failed.')
                utila.error(error)
                ret += 1
    return ret

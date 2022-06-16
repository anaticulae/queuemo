# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila.logger


def logger_start():
    tmp = configo.tmp(True)
    # create log folder
    queuemo_tmp = os.path.join(tmp, 'queuemo/log/')
    os.makedirs(queuemo_tmp, exist_ok=True)
    # determine current file name
    logfile = f'{utila.filetime()}_{utila.tmpname(10)}.log'
    outpath = os.path.join(queuemo_tmp, logfile)
    utila.debug(f'write global log to {outpath}')
    utila.logger.OUTFILE = outpath

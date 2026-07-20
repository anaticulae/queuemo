# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
import utilo.logger


def logger_start():
    tmp = configos.tmp()
    os.makedirs(tmp, exist_ok=True)
    # create log folder
    queuemo_tmp = os.path.join(tmp, 'queuemo/log/')
    os.makedirs(queuemo_tmp, exist_ok=True)
    # determine current file name
    logfile = f'{utilo.filetime()}_{utilo.tmpname(10)}.log'
    outpath = os.path.join(queuemo_tmp, logfile)
    utilo.debug(f'write global log to {outpath}')
    utilo.outfile_setup(outpath)

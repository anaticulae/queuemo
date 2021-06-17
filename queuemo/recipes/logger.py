# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila.logger

# TODO: MOVE TO SEPARATE FILE
LOGGERSTART = 0


def ensure_logger():
    if utila.logger.OUTFILE:
        return
    raise RuntimeError('no logger OUTFILE defined')


def start():
    ensure_logger()
    global LOGGERSTART  # pylint:disable=global-statement
    LOGGERSTART = utila.file_line_length(utila.logger.OUTFILE)


def content():
    ensure_logger()
    return utila.file_read_lines(utila.logger.OUTFILE, start=LOGGERSTART)


def complete():
    ensure_logger()
    return utila.file_read_lines(utila.logger.OUTFILE)

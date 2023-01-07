# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

# TODO: MOVE TO SEPARATE FILE
LOGGERSTART = 0


def ensure_logger():
    if utila.outfile():
        return
    raise RuntimeError('no outfile_setup defined')


def start():
    ensure_logger()
    global LOGGERSTART  # pylint:disable=global-statement
    LOGGERSTART = utila.file_line_length(utila.outfile())


def content() -> str:
    ensure_logger()
    loaded = utila.file_read_lines(utila.outfile(), start=LOGGERSTART)
    return loaded


def complete() -> str:
    ensure_logger()
    loaded = utila.file_read_lines(utila.outfile())
    return loaded

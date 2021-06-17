# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

STOPED = False


def isrunning():
    return not isstoped()


def isstoped() -> bool:
    return STOPED


def stop():
    utila.log('stop service')
    global STOPED  # pylint:disable=global-statement
    STOPED = True

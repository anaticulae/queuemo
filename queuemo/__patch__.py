# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila


def file_age(path: str) -> int:
    """\
    >>> file_age(__file__) > 0
    True
    """
    filetime = os.stat(path).st_mtime
    timediff = utila.now() - filetime
    timediff = int(timediff)
    return timediff


utila.file_age = file_age

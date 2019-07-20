# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from dataclasses import dataclass


@dataclass
class Step:
    process: str
    inpath: str
    outpath: str = ''


@dataclass
class Copy:
    source: str
    destination: str


@dataclass
class RawCopy(Copy):
    pass


@dataclass
class Publish(Copy):
    pass

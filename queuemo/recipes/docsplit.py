# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import join

from queuemo.recipes import PDF_FILE
from queuemo.recipes import RAWMAKER_OUTPUT
from queuemo.recipes import copy_content
from queuemo.recipes import rawmaker
from queuemo.recipes import sections

ONELINE_CHAR_MARGIN = 100.0  # TODO: HOLY VALUE
ONELINE_BOXES_FLOW = 1.0  # TODO: HOLY VALUE

DOCSPLIT_INPUT = 'sections_input'


def require():
    return 'extractraw'


def before(rawspace: str):
    rawmaker(
        rawspace,
        inpath=PDF_FILE,
        outpath=RAWMAKER_OUTPUT,
        prefix='oneline',
        char_margin=ONELINE_CHAR_MARGIN,
        boxes_flow=ONELINE_BOXES_FLOW,
        # run only this features
        font='',
        text='',
        toc='',
    )
    sectionspath = join(rawspace, DOCSPLIT_INPUT)

    copy_content(workingpath(rawspace), sectionspath)


def run(rawspace: str):
    sections(rawspace, DOCSPLIT_INPUT, DOCSPLIT_INPUT)


def workingpath(rawspace: str):
    result = join(rawspace, RAWMAKER_OUTPUT)
    return result

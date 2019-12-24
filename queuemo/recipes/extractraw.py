# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from queuemo.recipes import PDF_FILE
from queuemo.recipes import rawmaker

OUTPATH = 'rawmaker'


def run(rawspace: str):
    rawmaker(rawspace, PDF_FILE, pages='0:5')


def after(rawspace: str):
    # TODO: log health of extract document
    pass

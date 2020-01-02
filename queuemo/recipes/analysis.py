# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import join

from feedback.io import STATISTICA_CHAPTER_HTML
from feedback.io import STATISTICA_WORDS_HTML
from queuemo.recipes import GROUPME
from queuemo.recipes import analysis_statistica
from queuemo.recipes import copy
from queuemo.recipes import feedback_analysis_statistica
from queuemo.recipes import groupme
from queuemo.recipes import publish

ANALYSIS_STATISTICA = 'analysis_statistica'
FEED_STATISTICA = 'feedback_statistica'
FEED_STATISTICA_IN = '%s_input' % FEED_STATISTICA
RAWMAKER = 'rawmaker'


def require():
    return 'extractraw'


def before(rawspace: str):
    groupme(rawspace, RAWMAKER)
    # analysis_statistica(rawspace, GROUPME)


def run(rawspace: str):
    pass
    # input_ = [
    #     # ANALYSIS_STATISTICA,
    #     GROUPME,
    # ]
    # feedback_analysis_statistica(rawspace, input_)


def after(rawspace: str):
    # chapter_out = join(FEED_STATISTICA, STATISTICA_CHAPTER_HTML) + '.html'
    words_out = join(FEED_STATISTICA, STATISTICA_WORDS_HTML) + '.html'
    # publish(rawspace, chapter_out, 'statistica/chapter/sections')
    publish(rawspace, words_out, 'statistica/chapter/words')

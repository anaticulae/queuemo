# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Composition of recipes
======================

.. note :: outdated approach, TODO: UPDATE

DataMining: PDF ->
    RawMaker        -> text.yaml ->
    GroupMe         -> chapter.yaml ->

Analysis/Reporting:

    Statistica      -> statistic.yaml ->

Decider:

    MathStyle       -> style.yaml                   WordStyle

Feedback:

    Feedback        -> feedback.yaml                Feedback

Presentation:

    HTML VIEW
"""

import utila

import queuemo
import queuemo.runtime.scheduler

RECIPES = utila.join(queuemo.ROOT, 'queuemo', 'recipes', exist=True)


def create(name: str):
    path = utila.join(RECIPES, name, exist=True)
    loaded = queuemo.runtime.scheduler.load(path)
    return loaded


VALIDATION = create('validation')
FASTVIEW = create('fastview')
RESULT = create('result')
PUBLISH = create('publish')

ORDER = [
    VALIDATION,
    FASTVIEW,
    RESULT,
    PUBLISH,
]

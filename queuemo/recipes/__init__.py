# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
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
import os

import queuemo
import queuemo.runtime.scheduler

RECIPES = os.path.join(queuemo.ROOT, 'queuemo', 'recipes')

VALIDATION = queuemo.runtime.scheduler.load(os.path.join(RECIPES, 'validation'))
FASTVIEW = queuemo.runtime.scheduler.load(os.path.join(RECIPES, 'fastview'))
RESULT = queuemo.runtime.scheduler.load(os.path.join(RECIPES, 'result'))
PUBLISH = queuemo.runtime.scheduler.load(os.path.join(RECIPES, 'publish'))

ORDER = [
    VALIDATION,
    FASTVIEW,
    RESULT,
    PUBLISH,
]

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import queuemo
import queuemo.recipes.scheduler

EXAMPLE = os.path.join(queuemo.ROOT, 'tests/example/scheduler')
IMOM = os.path.join(EXAMPLE, 'imom')
ERRORNEOUS = os.path.join(EXAMPLE, 'erroneous')

for item in [EXAMPLE, IMOM, ERRORNEOUS]:
    assert os.path.exists(item), item


def test_recipe_scheduler_collect():
    collected = queuemo.recipes.scheduler.collect(IMOM)
    assert len(collected) == 5


def test_recipe_scheduler_collect_norunmethod(capsys):
    collected = queuemo.recipes.scheduler.collect(ERRORNEOUS)
    assert collected == {}
    error = capsys.readouterr().err
    assert 'could not load recipe step' in error, error


def test_recipe_scheduler_compose():
    collected = queuemo.recipes.scheduler.collect(IMOM)
    parent = 'example'

    composed = queuemo.recipes.scheduler.compose(collected, parent=parent)
    assert composed
    assert composed.before
    assert composed.main
    assert composed.after
    assert composed.failure
    assert composed.steps


def test_recipe_scheduler_schedule_alpha():
    """Test to schedule without scheduling order, use default alphabetic
    order"""
    items = [
        queuemo.recipes.scheduler.RecipeStep(name=name) for name in [
            'hello',
            'mister',
            'tom',
            'albert',
        ]
    ]
    expected = [
        queuemo.recipes.scheduler.RecipeStep(name=name) for name in [
            'albert',
            'hello',
            'mister',
            'tom',
        ]
    ]
    result = queuemo.recipes.scheduler.schedule(items)
    assert result == expected


def test_recipe_scheduler_schedule_mixed():
    order = ['mister', 'hello']
    steps = [
        queuemo.recipes.scheduler.RecipeStep(name=name) for name in [
            'tom',
            'hello',
            'mister',
            'albert',
        ]
    ]
    expected = [
        queuemo.recipes.scheduler.RecipeStep(name=name) for name in [
            'mister',
            'hello',
            'albert',
            'tom',
        ]
    ]
    result = queuemo.recipes.scheduler.schedule(steps, order)
    assert result == expected

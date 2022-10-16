# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import queuemo
import queuemo.runtime.scheduler

EXAMPLE = os.path.join(queuemo.ROOT, 'tests/example/scheduler')
IMOM = os.path.join(EXAMPLE, 'imom')
ERRORNEOUS = os.path.join(EXAMPLE, 'erroneous')

for item in [EXAMPLE, IMOM, ERRORNEOUS]:
    assert os.path.exists(item), item


def test_collect():
    collected = queuemo.runtime.scheduler.collect(IMOM)
    expected = {
        'after', 'bc_step', 'before', 'da_step', 'failure', 'main', 'runme'
    }
    current = set(collected.keys())
    assert current == expected


def test_collect_norunmethod(capsys):
    collected = queuemo.runtime.scheduler.collect(ERRORNEOUS)
    assert collected == {}  # pylint:disable=C1803
    error = capsys.readouterr().err
    assert 'could not load recipe step' in error, error


def test_load_and_order():
    """Ensure that uppercased ORDER is schedule correctly."""
    loaded = queuemo.runtime.scheduler.load(IMOM)
    names = [item.name for item in loaded.schedule]
    expected = ['before', 'main', 'da_step', 'bc_step', 'runme', 'after']
    assert names == expected


def test_compose():
    collected = queuemo.runtime.scheduler.collect(IMOM)
    parent = 'example'

    composed = queuemo.runtime.scheduler.compose(collected, parent=parent)
    assert composed
    assert composed.before
    assert composed.main
    assert composed.after
    assert composed.failure
    assert composed.steps


def test_schedule_alpha():
    """Test to schedule without order, use default alphabetic order."""
    items = [
        queuemo.runtime.scheduler.RecipeStep(name=name) for name in [
            'hello',
            'mister',
            'tom',
            'albert',
        ]
    ]
    expected = [
        queuemo.runtime.scheduler.RecipeStep(name=name) for name in [
            'albert',
            'hello',
            'mister',
            'tom',
        ]
    ]
    result = queuemo.runtime.scheduler.schedule(items)
    assert result == expected


def test_schedule_mixed():
    order = ['mister', 'hello']
    steps = [
        queuemo.runtime.scheduler.RecipeStep(name=name) for name in [
            'tom',
            'hello',
            'mister',
            'albert',
        ]
    ]
    expected = [
        queuemo.runtime.scheduler.RecipeStep(name=name) for name in [
            'mister',
            'hello',
            'albert',
            'tom',
        ]
    ]
    result = queuemo.runtime.scheduler.schedule(steps, order)
    assert result == expected

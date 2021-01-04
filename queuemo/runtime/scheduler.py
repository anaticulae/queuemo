# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Scheduler
=========

Steps
-----

 1. Before
 2. (main) -> Run if defined.

  a. step a
  b. step b
  c. step ...

 3. After
 4. Failure -> Run if some step fails

Before
~~~~~~

Main
~~~~

Main is runned only if defined. In the main part there is the option to
schedule to define the order of the executed steps. If no **ORDER** is
defined an alphabetical order is used.

After
~~~~~

Failure
~~~~~~~

If defined it is runned if some error occurs in any step.

Scheduler
---------

Define order, prefix and parallizeability of executed jobs

ORDER = [
    'titlepage'
]

ORDER = [
    ('01', titlepage')
]

ORDER = [
    {
        'titlepage', 'paper',
    },
    {
        'toc',
    }
]
"""

import contextlib
import dataclasses
import importlib
import importlib.util
import os
import typing

import utila


@dataclasses.dataclass
class RecipeStep:
    name: str = None
    prefix: str = None
    before: callable = None
    run: callable = None
    after: callable = None


RecipeSteps = typing.List[RecipeStep]

ORDER = 'ORDER'


def required(func):
    func.required = True
    return func


def isrequired(func):
    return hasattr(func, 'required')


@dataclasses.dataclass
class ComposedRecipe:

    name: str = None
    before: RecipeStep = None
    main: RecipeStep = None
    steps: typing.List[RecipeStep] = dataclasses.field(default_factory=list)
    after: RecipeStep = None
    failure: RecipeStep = None

    @property
    def schedule(self) -> list:
        result = []
        if self.before:
            result.append(self.before)
        if self.main:
            result.append(self.main)
            if self.steps:
                order = getattr(self.main, ORDER.lower(), None)
                scheduled = schedule(self.steps, order)
                result.extend(scheduled)
        else:
            if self.steps:
                result.extend(self.steps)
        if self.after:
            result.append(self.after)
        return result

    def __getitem__(self, index):
        return self.schedule[index]

    def __iter__(self):
        return iter(self.schedule)

    def __len__(self):
        return len(list(self.schedule))

    def append(self, item):
        self.steps.append(item)  # pylint:disable=E1101


def collect(path: str) -> dict:
    """Collect recipe steps from `path`. Ignore file which does not
    contain a run method.

    Args:
        path(str): collect python files from folder
    Returns:
        dict[name] = recipe
    """
    items = [
        item for item in os.listdir(path)
        if item.endswith('.py') and item != '__init__.py'
    ]
    result = {}
    parent = os.path.basename(path)
    for item in items:
        item = item[0:-3]
        spec = importlib.util.spec_from_file_location(
            f'{parent}.{item}',
            os.path.join(path, f'{item}.py'),
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, 'run'):
            utila.error(f'could not load recipe step: `{item}` in `{path}`')
            continue

        step = RecipeStep(name=item)
        for value_name in ['before', 'run', 'after', ORDER, 'PREFIX']:
            with contextlib.suppress(AttributeError):
                value = getattr(module, value_name)
                value_name = value_name.lower()
                setattr(step, value_name, value)
        result[item] = step
    return result


def compose(collected: dict, parent: str) -> ComposedRecipe:
    """Match file name with RecipeSteps.

    Possible steps are: before, (main), (steps...), after and failure.
    """
    result = ComposedRecipe(name=parent)

    standard = set(['before', 'main', 'after', 'failure'])
    for item in standard:
        with contextlib.suppress(KeyError):
            setattr(result, item, collected[item])

    for key, value in collected.items():
        if key in standard:
            continue
        result.append(value)
    return result


def load(path: str) -> ComposedRecipe:
    """Compose recipe from path.

    Load recipse and compose them afterwards to run in `runner`.
    """
    assert os.path.exists(path), path
    parent = os.path.basename(path)
    collected = collect(path)
    composed = compose(collected, parent=parent)
    return composed


def schedule(steps: RecipeSteps, orderby: list = None) -> RecipeSteps:
    """Define the order of given `steps`.

    If **no orderby** is given, return steps alphabetically sorted.
    If **orderby** is given, sort steps by `orderby` and the rest
    alphabetically.

    Args:
        steps(list): steps to order
        orderby(list): list of RecipeSteps.name's
    Returns:
        sorted `steps`
    """
    steps = steps[:]  # copy to avoid changing source list
    steps = sorted(steps, key=lambda x: x.name)
    if orderby is None:
        return steps

    find = {step.name: step for step in steps}

    result = []
    for index, item in enumerate(orderby):
        try:
            found = find[item]
        except KeyError:
            utila.error(f'could not schedule {index} {item}')
        else:
            result.append(found)
            steps.remove(found)
    # add unscheduled tasks
    result.extend(steps)
    return result

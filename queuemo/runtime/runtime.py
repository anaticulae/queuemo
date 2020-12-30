# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Runtime
=======

The runtime executes the defined schedules and organizes the creation of
paths and the dataflow between the recipe steps.

API
---

- Name of used folder and job is defined by location and file name
"""

import os

import utila
import utila.logger

import queuemo
import queuemo.runtime.api
import queuemo.runtime.scheduler
import queuemo.utils


class RecipeRuntime:
    """The RecipeRuntime manages to executes a list of ComposedRecipes."""

    def __init__(
            self,
            workspace: str,
            document: str,
            outpath: str,
            failfast: bool = False,
    ):
        """Initialize RectipeRuntime.

        Args:
            workspace(str): path which contains the `document` and where
                            the temporary files are created
            document(str): identifier of processed document
            outpath(str): write results to
            failfast(bool): shut down scheduler on first error
        """
        self.todo = []
        self.workspace = workspace
        self.document = document
        self.outpath = outpath
        self.failfast = failfast

    def append(self, item: queuemo.runtime.scheduler.ComposedRecipe):
        """Add composed recipe to todo list"""
        assert isinstance(item, queuemo.runtime.scheduler.ComposedRecipe), item
        self.todo.append(item)

    def next_step(self, tick=None) -> bool:
        """Run next composed recipe.

        Returns:
            - None if todo is empty
            - True if ComposedRecipe is executed successfully
            - False if execution raised an RuntimeError
        """
        if not self.todo:
            return None
        current = self.todo.pop(0)
        try:
            tmppath = os.path.join(self.workspace, current.name)
            if self.outpath:
                outpath = os.path.join(self.outpath, current.name)
            else:
                outpath = None
            flow = queuemo.runtime.api.RecipeIO(
                workspace=self.workspace,
                document=self.document,
                tmppath=tmppath,
                outpath=outpath,
            )
            run(current, flow, tick=tick, failfast=self.failfast)
            if tick:
                tick()
        except RuntimeControl as error:
            utila.info(error)
            # TODO Should we return NONE, to signal that process is over?
            return False
        except RuntimeError as error:
            utila.error(error)
            return False
        return True

    def finish(self, tick=None):
        assert self.todo, 'nothing todo'
        current = None
        while self.todo:
            current = self.next_step(tick)
        return current

    def __len__(self):
        return len(self.todo)

    def __getitem__(self, index):
        return self.todo[index]


class RuntimeControl(RuntimeError):
    pass


class Stop(RuntimeControl):
    pass


def run(  # pylint:disable=R1260
        composition: queuemo.runtime.scheduler.ComposedRecipe,
        flow: queuemo.runtime.api.RecipeIO,
        tick: callable = None,
        failfast: bool = False,
):
    """Run composed steps in the order defined by `Scheduler`.
    Use `flow` to determine the location where data must copy to.

    There are 2 types of steps, the standard steps: before, main and
    after. These steps works on the general `composition.name/.tmp`
    location. The other steps which are defined by the user works und
    the `tmppath` `composition.name/recipestep.name`.

    The output data is written to `outpath/recipestep.name` these name
    can be prefixed if file defined the global constant `PREFIX`.
    These path results in `outpath/PREFIX_recipestep.name`.

    The running order of the methods for every RecipseStep is **before,
    run, after**. These steps are always optional. In the case of an
    error in one of these steps an RuntimeError is raised which must be
    handled by `RecipeRuntime`.

    Args:
        composition: composed recipe which is loaded from an local path
        flow: define the location where data transfer must handled
        tick: inform user about step progress
        failfast: ignore required flag. Shut down scheduler by first error
    Raises:
        RuntimeError: if some failure occurs while executing a RecipeStep
        RuntimeControl: if some step signals to hold
    """
    tmp = os.path.join(flow.tmppath, '.tmp')
    print_banner(composition.name, symbol='@')
    for current in composition.schedule:
        print_banner(current.name, symbol='*')
        name = current.name
        if current.prefix:
            # add prefix to result of scheduling step
            name = f'{current.prefix}_{current.name}'
        tmppath = os.path.join(flow.tmppath, name)
        outpath = os.path.join(flow.outpath, name) if flow.outpath else None
        if current.name in ['before', 'after', 'main']:  # TODO: INCLUDE PREFIX?
            tmppath = tmp
            outpath = flow.outpath
        current_flow = queuemo.runtime.api.RecipeIO(
            workspace=flow.workspace,
            document=flow.document,
            tmppath=tmppath,
            outpath=outpath,
        )
        os.makedirs(tmppath, exist_ok=True)
        for item in ['before', 'run', 'after']:
            action = getattr(current, item)
            if action is None:
                continue
            utila.call(item)
            try:
                utila.debug(current_flow)
                action(current_flow)
            except RuntimeControl as control:
                raise control
            except Exception as error:  # pylint:disable=broad-except
                utila.error(f'could not run: {item}')
                utila.error(error)
                utila.logger.log_stacktrace()
                if queuemo.isrequired(action) or failfast:
                    # do not stop scheduler if step is not marked as
                    # required.
                    raise RuntimeError(f'{current.name}:{item}') from error
        if queuemo.INTERACTIVE:
            queuemo.utils.wait()
        if tick:
            tick()


def print_banner(text, symbol='*'):
    utila.log('\n' + symbol * 80)
    utila.log(f'{text}'.center(80))
    utila.log(symbol * 80 + '\n')

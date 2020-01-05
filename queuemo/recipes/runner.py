# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import queuemo.recipes.api
import queuemo.recipes.scheduler


class RecipeRuntime:

    def __init__(self, flow: queuemo.recipes.api.RecipeIO):
        self.todo = []
        self.flow = flow

    def append(self, item):
        self.todo.append(item)

    def next_step(self):
        if not self.todo:
            return None
        current = self.todo.pop()
        try:
            run(current, self.flow)
        except RuntimeError:
            return False
        return True

    def __len__(self):
        return len(self.todo)


def run(
        composition: queuemo.recipes.scheduler.ComposedRecipe,
        flow: queuemo.recipes.api.RecipeIO,
):  # pylint:disable=R1260
    for current in composition.schedule:
        utila.info(f'run {current.name}')
        if current.before:
            utila.call('before')
            try:
                current.before(flow)
            except Exception as error:
                utila.error(error)
                raise RuntimeError(f'{current.name}: before')

        if current.run:
            utila.call('run')
            try:
                current.run(flow)
            except Exception as error:
                utila.error(error)
                raise RuntimeError(f'{current.name}: run')

        if current.after:
            utila.call('after')
            try:
                current.after(flow)
            except Exception as error:
                utila.error(error)
                raise RuntimeError(f'{current.name}: after')

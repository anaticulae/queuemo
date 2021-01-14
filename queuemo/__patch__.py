# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import functools

import utila


class GeorgFork(contextlib.AbstractContextManager):
    """Fork methods to run in parallel."""

    def __init__(
            self,
            process: bool = True,
            returncode: bool = True,
            worker: int = None,
    ):
        self.process = process
        self.worker = worker
        self.returncode = returncode
        self.todo = []
        self.result = None

    def fork(self, method, **kwargs):
        runme = functools.partial(method, **kwargs)
        self.todo.append(runme)

    def __exit__(self, exc_type, exc_value, traceback):
        # run schedule
        self.result = utila.fork(
            *self.todo,
            process=self.process,
            returncode=self.returncode,
            worker=len(self.todo) if self.worker is None else self.worker,
        )


utila.GeorgFork = GeorgFork

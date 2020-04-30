# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import dataclasses
import os
import textwrap

import link
import utila


@dataclasses.dataclass
class RecipeIO:
    workspace: str = None
    document: str = None
    tmppath: str = None
    outpath: str = None

    @property
    def sourcepath(self) -> str:
        """Path where pdf document is stored with file extention."""
        todo = link.todo(self.document)
        resource = os.path.join(todo, self.document)
        assert os.path.exists(resource), resource
        return resource

    @property
    def general(self) -> str:
        if self.tmppath.endswith('.tmp'):
            return self.tmppath
        result = os.path.join(self.tmppath, '../.tmp')
        return result

    @property
    def main(self) -> str:
        parent = os.path.join(self.outpath, '..')
        return parent

    def package(self, item) -> str:
        """Path to package step."""
        parent = os.path.split(self.tmppath)[0]
        path = os.path.join(parent, item)
        assert os.path.exists(path), path
        return path

    def publish_linting(self, fastview: bool = True, verbose: bool = False):
        """Publish to fastview and if exists to result also"""
        if fastview:
            utila.copy_content(
                self.tmppath,
                self.outpath,
                pattern='*_user.yaml',
                verbose=verbose,
            )
        resultview = link.resultview(self.document)
        # TODO: CHECK TO AVOID COPING DOUBLE WHEN USING IN RESULT VIEW
        if os.path.exists(resultview):
            utila.copy_content(
                self.tmppath,
                resultview,
                pattern='*_user.yaml',
                verbose=verbose,
            )
        assert fastview or os.path.exists(resultview), 'no copy executed'

    def publish_main(self, folder=None, pattern='*.*'):
        source = self.tmppath
        if folder is not None:
            source = os.path.join(self.tmppath, folder)
        utila.copy_content(source, self.main, pattern=pattern)

    def publish(self, folder=None, pattern='*.*'):
        source = self.tmppath
        if folder is not None:
            source = os.path.join(self.tmppath, folder)
        utila.copy_content(source, self.outpath, pattern=pattern)

    def __str__(self):
        return textwrap.dedent(f"""\
            document:   {self.document}
            general:    {self.general}
            main:       {self.main}
            outpath:    {self.outpath}
            sourcepath: {self.sourcepath}
            tmppath:    {self.tmppath}
            workspace:  {self.workspace}
        """)

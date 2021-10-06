# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Runtime API
===========

PathStructure
-------------

WorkDir
    Workspace document z4YgqnjU0Q6dCa5r
        z4YgqnjU0Q6dCa5r: pdf file with content
        fastview
        result
            imgfig
            intro
            view
        pdfinfo.yaml
        inprogress
        jobinfo.yaml
    Workspace document Bobomaster
        ...
        ...
        ...
        pdfinfo.yaml
        inprogress
        jobinfo.yaml

TmpDir
    z4YgqnjU0Q6dCa5r
    Bobomaster
"""

import dataclasses
import os
import textwrap

import link
import utila


@dataclasses.dataclass
class RecipeConfig:
    failfast: bool = False
    # do not analyze not supported documents
    skip_unsupported: bool = False
    verbose: bool = True


@dataclasses.dataclass
class RecipeIO:
    workspace: str = None
    # documentid
    document: str = None
    tmppath: str = None
    outpath: str = None
    config: RecipeConfig = None

    @property
    def sourcepath(self) -> str:
        """Path where pdf document is stored without file extention."""
        resource = os.path.join(self.todopath, self.document)
        assert os.path.exists(resource), resource
        return resource

    @property
    def general(self) -> str:
        if self.tmppath.endswith('.tmp'):
            return self.tmppath
        result = os.path.join(self.tmppath, '../.tmp')
        result = os.path.normpath(result)
        return result

    @property
    def main(self) -> str:
        if not self.outpath:
            return None
        parent = os.path.join(self.outpath, '..')
        parent = os.path.normpath(parent)
        return parent

    @property
    def todopath(self) -> str:
        return link.todo(self.document)

    def package(self, item) -> str:
        """Path to package step."""
        parent = os.path.split(self.tmppath)[0]
        path = os.path.join(parent, item)
        assert os.path.exists(path), path
        return path

    def publish_linting(self, verbose: bool = False):
        """Publish to fastview and if exists to result also"""
        if not self.outpath:
            utila.log('skip publishing')
            return
        utila.copy_content(
            self.tmppath,
            self.outpath,
            pattern='*_user.yaml',
            verbose=verbose,
        )

    def publish(self, folder=None, pattern='*.*'):
        source = self.tmppath
        if folder is not None:
            source = os.path.join(self.tmppath, folder)
        if self.outpath:
            utila.copy_content(source, self.outpath, pattern=pattern)
        else:
            todo = link.todo(self.document)
            utila.copy_content(source, todo, pattern=pattern)

    def __str__(self):
        return textwrap.dedent(f"""\
            document:   {self.document}
            general:    {self.general}
            main:       {self.main}
            outpath:    {self.outpath}
            sourcepath: {self.sourcepath}
            tmppath:    {self.tmppath}
            workspace:  {self.workspace}
            todopath:   {self.todopath}
        """)

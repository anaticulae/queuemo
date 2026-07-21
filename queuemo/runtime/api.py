# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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

import iamraw
import qvlink
import serializeraw
import utilo


@dataclasses.dataclass
class RecipeConfig:
    failfast: bool = False
    # do not analyze not supported documents
    skip_unsupported: bool = False
    webconfig: iamraw.WebConfig = None
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
    def docinfo(self) -> str:
        # docinfo
        loaded = serializeraw.load_docinfo(self.general)
        if not loaded:
            return None
        result = ''
        # bachelor64ger
        # bachelor64german
        # TODO: USE DOCINFO->STR CONVERTER
        if loaded.pages:
            result = f'{loaded.pages}'
        if loaded.lang:
            result = f'{result}{loaded.lang.name.lower()}'
        return result

    @property
    def docinfo_ifgiven(self) -> dict:
        if self.docinfo:
            return {'docinfo': self.docinfo}
        return {}

    @property
    def sourcepath(self) -> str:
        """Path where pdf document is stored without file extention."""
        resource = os.path.join(self.todopath, self.document)
        assert os.path.exists(resource), resource
        return resource

    @property
    def general(self) -> str:
        # TODO: RENAME TO TMP_COMMON
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
        return qvlink.todo(self.document)

    def package(self, item) -> str:
        """Path to package step."""
        parent = os.path.split(self.tmppath)[0]
        path = os.path.join(parent, item)
        assert os.path.exists(path), path
        return path

    def publish_linting(self, verbose: bool = False):
        """Publish to fastview and if exists to result also"""
        if not self.outpath:
            utilo.log('skip publishing')
            return
        utilo.copy_content(
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
            utilo.copy_content(source, self.outpath, pattern=pattern)
        else:
            todo = qvlink.todo(self.document)
            utilo.copy_content(source, todo, pattern=pattern)

    def skip(self, decider: str) -> bool:
        if not self.config:
            return False
        webconfig: iamraw.WebConfig = self.config.webconfig
        if not webconfig:
            return False
        if not webconfig.decider:
            return False
        if not isinstance(decider, str):
            decider = decider.__name__
        if decider in webconfig.decider:
            return False
        return True

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

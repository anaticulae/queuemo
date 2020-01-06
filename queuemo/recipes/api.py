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
        resource = os.path.join(self.workspace, self.document)
        assert os.path.exists(resource), resource
        return resource

    @property
    def general(self) -> str:
        if self.tmppath.endswith('.tmp'):
            return self.tmppath
        return os.path.join(self.tmppath, '../.tmp')

    def publish_linting(self):
        utila.copy_content(self.tmppath, self.outpath, pattern='*_user.yaml')

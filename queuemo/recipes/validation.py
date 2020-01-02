# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila


def run(workspace: str, document):
    """Run validation to check that """
    ressource = os.path.join(workspace, document)
    assert os.path.exists(ressource), str(ressource)

    outpath = os.path.join(configo.todo(True), document)

    utila.log(f'validate: {ressource}')
    completed = utila.run(f'pdfinfo -i {ressource} -o {outpath}')
    utila.log(f'write validation result to: {outpath}')

    if completed.returncode:
        utila.error(completed.stderr + completed.stdout)
    assert completed.returncode == 0

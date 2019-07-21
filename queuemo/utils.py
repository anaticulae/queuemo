# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here"""

from os import listdir
from os import makedirs
from os.path import basename
from os.path import exists
from os.path import isfile
from os.path import join
from shutil import copy

from utila import file_create
from utila import file_read


def isfilepath(path: str):
    assert path, path
    if exists(path):
        return isfile(path)
    base = basename(path)
    if base[0] == '.':
        # .tmp
        return False
    return '.' in base


def copy_content(source: str, destination: str, recursive: bool = False):
    """Copy the content from `source` to `destination` folder. If `desitination`
    folder does not exists, it will be created.

    Hint:
        Why not using shutil.copytree?: Copy tree expect that destination does
        not exists, but we need this.
    """
    assert exists(source), str(source)
    if isfile(source):
        content = file_read(source)
        if not isfilepath(destination):
            makedirs(destination, exist_ok=True)
            destination = join(destination, basename(source))
        file_create(destination, content)
        return

    makedirs(destination, exist_ok=True)
    for item in listdir(source):
        source_ = join(source, item)
        dest_ = join(destination, item)
        if isfile(source_):
            # copy files
            copy(source_, dest_)
        else:
            # 'copy' folder
            makedirs(dest_)
            if recursive:
                copy_content(source_, dest_, recursive=True)

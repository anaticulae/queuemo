# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import glob
import os

import utila
from utila.utils import chdir


def copy_content(
        source: str,
        destination: str,
        pattern: str = None,
        *,
        verbose: bool = False,
        recursive: bool = False,
        skip_overwrite: bool = False,
):
    """Copy the content from `source` to `destination` folder. If
    `destination` folder does not exists, it will be created.

    Hint:
        Why not using shutil.copytree?: Copy tree expect that
        destination does not exists, but we need this.

    Args:
        source(str): file or directory to copy
        destination(str): directory to copy source item(s)
        pattern(str): accept files which matches this pattern, if None
                      all files matches.
        recursive(bool): if True, copy child folder
        skip_overwrite(bool): if file exists and is not changed, do
                              nothing.
        verbose(bool): If True, log executed operation
    """
    if os.path.isfile(source):
        if not utila.isfilepath(destination):
            destination = os.path.join(destination, os.path.basename(source))
        if verbose:
            utila.log(f'cp: {source} -> {destination}')
        utila.file_copy(
            source,
            destination,
            skip_overwrite=skip_overwrite,
        )
        return

    if pattern is None:
        pattern = '*'
    pattern = f'**/{pattern}' if recursive else pattern

    with chdir(source):
        selected = list(glob.glob(pattern, recursive=recursive))

    for item in selected:
        source_ = os.path.join(source, item)
        dest_ = os.path.join(destination, item)
        if os.path.isfile(source_):
            if verbose:
                utila.log(f'cp: {source_} -> {dest_}')
            utila.file_copy(source_, dest_, skip_overwrite=skip_overwrite)
        else:
            if verbose:
                utila.log(f'mkdir: {dest_}')
            os.makedirs(dest_, exist_ok=True)

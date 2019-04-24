# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import file_replace
from utila import from_raw_or_path
from yaml import dump
from yaml import load
from yaml.loader import SafeLoader


def read(content: str):
    raw = from_raw_or_path(content)
    loaded = load(raw, Loader=SafeLoader)
    return loaded


def write(path: str, config: dict):
    dumped = dump(config)
    file_replace(path, dumped)

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import raises

from queuemo.tabstructure import TabStructure
from queuemo.tabstructure import load

EXAMPLE = \
"""
statistica:6
    error:2
    style:3
        table:1
        fonts:2
        chapter:10
    chapter:5
        words:4
            index.html->erwin.txt

rawmaker:4
    words:2
gomaker:2
    abc:1
"""


def test_tabstructure_load_and_lookup():
    loaded: TabStructure = load(EXAMPLE)

    assert loaded.look('rawmaker/words') == '04_rawmaker/02_words/'

    assert loaded.look(
        'statistica/chapter/words') == '06_statistica/05_chapter/04_words/'

    assert loaded.look('statistica/error') == '06_statistica/02_error/'

    assert loaded.look('gomaker') == '02_gomaker/'

    with raises(ValueError):
        loaded.look('non_existing_path')

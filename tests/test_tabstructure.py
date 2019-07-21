# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
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

    assert loaded.look('rawmaker/words') == 'rawmaker_04/words_02/'

    assert loaded.look(
        'statistica/chapter/words') == 'statistica_06/chapter_05/words_04/'

    assert loaded.look('statistica/error') == 'statistica_06/error_02/'

    assert loaded.look('gomaker') == 'gomaker_02/'

    with raises(ValueError):
        loaded.look('non_existing_path')

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here."""

import os

import capita.path
import serializeraw


def select_pages(path: str, select, noselect=None) -> str:
    """\
    Support merging multiple selected pages.
    """
    assert_classes(select)
    path = capita.path.result(path)
    sectionx = serializeraw.load_sections(path)
    if not noselect:
        noselect = {}
    pages = select_section(
        sectionx,
        select=select,
        noselect=noselect,
    )
    if pages:
        pages = pages2str(pages)
        return pages
    return ':'


def select_section(sectionx, select, noselect) -> tuple:
    assert_classes(select)
    # flatten sections
    flat = []
    for level in sectionx:
        # TODO: REPLACE WITH NICE ITERATOR TO IMPROVE CODE STYLE
        flat.append(level)
        flat.extend(level[:])
    # select region
    collected = []
    for item in flat:
        if inside(item.__class__, noselect):
            continue
        if inside(item.__class__, select):
            collected.append((item.start, item.end))
    return collected


def inside(item, container) -> bool:
    if item == container:
        return True
    if isinstance(container, (tuple, list)) and item in container:
        return True
    return False


def pages2str(pages: tuple) -> str:
    """Merges tuple or list of tuples to `cli` --pages format.

    >>> pages2str((5,5))
    '5'
    >>> pages2str((1,5))
    '1:5'
    >>> pages2str([(1,5), (9,9)])
    '1:5,9'
    """
    if isinstance(pages, list):
        collected = [pages2str(item) for item in pages]
        return ','.join(collected)
    if (pages[0]) == pages[1]:
        return str(pages[0])
    return ':'.join([str(item) for item in pages])


def exists(filename: str, sources: list) -> bool:
    return any(os.path.exists(os.path.join(source, filename)) for source in sources)  # yapf:disable


def assert_classes(items):
    """\
    >>> import iamraw.sections
    >>> assert_classes(iamraw.sections.Bibliography)
    >>> assert_classes((iamraw.sections.Bibliography, iamraw.sections.Appendix))
    """
    if isinstance(items, (list, tuple)):
        for item in items:
            assert_classes(item)
        return
    assert isinstance(items, object.__class__), f'class not: {type(items)}'

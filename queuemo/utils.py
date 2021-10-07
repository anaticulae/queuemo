# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here."""

import importlib.util
import os
import sys

import sections.path
import serializeraw
import utila


def select_pages(path: str, select) -> str:
    """\
    Support merging multiple selected pages.
    """
    assert_classes(select)
    path = sections.path.result(path)
    sectionx = serializeraw.load_sections(path)
    pages = select_section(sectionx, select=select)
    if pages:
        pages = pages2str(pages)
        return pages
    return ':'


def select_section(sectionx, select) -> tuple:
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


def wait():
    """Ask user to continue program."""
    answer = input('continue?\n')
    answer = answer.strip().lower()
    if answer in ('no', 'n'):
        sys.exit(utila.SUCCESS)


def exists(filename: str, sources: list) -> bool:
    for source in sources:
        if os.path.exists(os.path.join(source, filename)):
            return True
    return False


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


def load_module(path: str):
    """\
    >>> load_module(__file__).__name__
    'queuemo.utils'
    """
    item = utila.file_name(path)
    parent = utila.file_name(utila.path_parent(path))
    spec = importlib.util.spec_from_file_location(
        f'{parent}.{item}',
        path,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

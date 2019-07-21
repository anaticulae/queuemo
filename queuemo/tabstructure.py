# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Example:

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
"""

SPLIT_LEVEL = '    '  # 4 space per level

FORWARD_SLASH = '/'


class TabStructure:
    """Slow and not very nice, but the file format works it out! :)"""

    # TODO: Support adapterfile
    def __init__(self, data):
        self.data = data

    def look(self, path: str):
        assert path
        splitted = path.split(FORWARD_SLASH)
        current = self.data

        result = ''
        for item in splitted:
            children = current['children']
            for search in children:
                if search['name'] == item:
                    result += '%s_%s/' % (search['name'], search['number'])
                    current = search
                    break
            else:
                raise ValueError('could not locate: %s' % path)
        return result


def load(raw: str) -> TabStructure:
    splitted = raw.splitlines()

    current = {'name': 'root', 'level': -1, 'children': []}
    stack = []
    for item in splitted:
        if not item:
            continue
        level = item.count(SPLIT_LEVEL)
        item = item.strip()
        try:
            text, number = item.split(':')
        except ValueError:
            continue
        else:
            number = number.zfill(2)

        this = {'name': text, 'number': number, 'level': level, 'children': []}
        if level > current['level']:
            current['children'].append(this)
            stack.append(current)
            current = this
            continue
        while level <= current['level']:
            current = stack.pop()
        current['children'].append(this)
        stack.append(current)
        current = this
    root = stack[0]
    init = TabStructure(root)
    return init

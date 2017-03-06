#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

resource_filename = __import__('pkg_resources').resource_filename

_emoji_chars = None


def emoji_chars(*args):
    """
    return a sequence with emoji ranges
    """
    global _emoji_chars
    if _emoji_chars is None:
        data = set()
        source = resource_filename(__name__, 'EmojiSources.txt')
        with open(source, "rU") as f:
            for s in f.readlines():
                s = s.strip()
                if not s or s.startswith('#'):
                    continue
                sequence = s.split(';')[0]  # 0: Unicode code point or sequence
                splits = []
                for s in sequence.split():
                    s = '\\U' + s.rjust(8, '0')  # pad to 10 char length
                    splits.append(s.decode('unicode-escape'))  # UTF-8
                data.add(''.join(splits))
        _emoji_chars = frozenset(data)
    return _emoji_chars


def has_emoji_chars(s):
    try:
        source = s.decode('utf-8')
    except UnicodeEncodeError:
        source = s
    for c in emoji_chars():
        if c in source:
            return True
    return False
has_emoji = has_emoji_chars  # BWC

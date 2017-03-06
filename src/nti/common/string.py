#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

resource_filename = __import__('pkg_resources').resource_filename

#: Digit chars
DIGITS = "0123456789"

#: ASCII uppercase chars
ASCII_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#: ASCII lowercase chars
ASCII_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"

#: ASCII letter chars
ASCII_LETTERS = ASCII_LOWERCASE + ASCII_UPPERCASE

#: White space chars
WHITESPACE = "\t\n\x0b\x0c\r "

#: Regular punk chars
PUNCTUATION = """!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""

#: True values chars
TRUE_VALUES = ('1', 'y', 'yes', 't', 'true', 'on')

#: False values chars
FALSE_VALUES = ('0', 'n', 'no', 'f', 'false', 'off')

try:
    _unicode = unicode
except NameError:  # python 3
    _unicode = lambda s: s


def is_true(t):
    result = bool(t and str(t).lower() in TRUE_VALUES)
    return result


def is_false(t):
    result = bool(t is not None and str(t).lower() in FALSE_VALUES)
    return result


def unicode_(s, encoding='utf-8', err='strict'):
    """
    Decode a byte sequence and unicode result
    """
    s = s.decode(encoding, err) if isinstance(s, bytes) else s
    return _unicode(s) if s is not None else None
safestr = to_unicode = unicode_  # BWC

_emoji_chars = None


import zope.deferredimport
zope.deferredimport.initialize()

zope.deferredimport.deprecatedFrom(
    "Moved to nti.common.emoji",
    "nti.common.emoji",
    "emoji_chars",
    "has_emoji",
    "has_emoji_chars"
)

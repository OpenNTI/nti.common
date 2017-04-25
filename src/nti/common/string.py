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
WHITESPACE = u"\t\n\x0b\x0c\r "

#: Regular punk chars
PUNCTUATION = """!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""

#: True values chars
TRUE_VALUES = ('1', 'y', 'yes', 't', 'true', 'on')

#: False values chars
FALSE_VALUES = ('0', 'n', 'no', 'f', 'false', 'off')


def is_true(t):
    result = bool(t and str(t).lower() in TRUE_VALUES)
    return result


def is_false(t):
    result = bool(t is not None and str(t).lower() in FALSE_VALUES)
    return result


import zope.deferredimport
zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Import from nti.base._compat instead",
    safestr='nti.base._compat:text_',
    unicode_='nti.base._compat:text_',
    to_unicode='nti.base._compat:text_',)


zope.deferredimport.deprecatedFrom(
    "Moved to nti.common.emoji",
    "nti.common.emoji",
    "has_emoji",
    "has_emoji_chars"
)

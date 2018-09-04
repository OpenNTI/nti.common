#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six
import unicodedata

from nti.common._compat import text_

import zope.deferredimport

resource_filename = __import__('pkg_resources').resource_filename

#: Digit chars
DIGITS = u"0123456789"

#: ASCII uppercase chars
ASCII_UPPERCASE = u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#: ASCII lowercase chars
ASCII_LOWERCASE = u"abcdefghijklmnopqrstuvwxyz"

#: ASCII letter chars
ASCII_LETTERS = ASCII_LOWERCASE + ASCII_UPPERCASE

#: White space chars
WHITESPACE = u"\t\n\x0b\x0c\r "

#: Regular punk chars
PUNCTUATION = u"""!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""

#: True values chars
TRUE_VALUES = ('1', 'y', 'yes', 't', 'true', 'on')

#: False values chars
FALSE_VALUES = ('0', 'n', 'no', 'f', 'false', 'off')

logger = __import__('logging').getLogger(__name__)


def is_true(t):
    result = bool(t and str(t).lower() in TRUE_VALUES)
    return result


def is_false(t):
    result = bool(t is not None and str(t).lower() in FALSE_VALUES)
    return result


if six.PY3:  # pragma: no cover
    def normalize_caseless(text):
        return unicodedata.normalize("NFKD", text.casefold())
else:  # pragma: no cover
    def normalize_caseless(text):
        return unicodedata.normalize("NFKD", text_(text).lower())


def equals_ignore_case(left, right):
    return (left == right) or normalize_caseless(left) == normalize_caseless(right)


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

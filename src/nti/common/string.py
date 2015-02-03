#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

DIGITS = "0123456789"

ASCII_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ASCII_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
ASCII_LETTERS = ASCII_LOWERCASE + ASCII_UPPERCASE

WHITESPACE = "\t\n\x0b\x0c\r "

PUNCTUATION = """!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
PRINTABLE = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c"""

TRUE_VALUES = ('1', 'y', 'yes', 't', 'true')
FALSE_VALUES = ('0', 'n', 'no', 'f', 'false')

def safestr(s):
    s = s.decode("utf-8") if isinstance(s, bytes) else s
    return unicode(s) if s is not None else None

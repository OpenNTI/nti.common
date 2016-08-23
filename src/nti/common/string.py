#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six

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

#: Printable punk chars
PRINTABLE = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c"""

#: True values chars
TRUE_VALUES = ('1', 'y', 'yes', 't', 'true')

#: False values chars
FALSE_VALUES = ('0', 'n', 'no', 'f', 'false')

def is_true(t):
	result = bool(t and str(t).lower() in TRUE_VALUES)
	return result

def is_false(t):
	result = bool(t is not None and str(t).lower() in FALSE_VALUES)
	return result

def to_unicode(s, encoding='utf-8', err='strict'):
	"""
	Decode a byte sequence and unicode result
	"""
	s = s.decode(encoding, err) if isinstance(s, bytes) else s
	return six.u(s) if s is not None else None
safestr = to_unicode # BWC

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
				sequence = s.split(';')[0] # 0: Unicode code point or sequence
				splits = []
				for s in sequence.split():
					s = '\\U' + s.rjust(8, '0') # pad to 10 char length
					splits.append(s.decode('unicode-escape')) # UTF-8
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
has_emoji = has_emoji_chars # BWC

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deals with a lot of cross-version issues.

Taken from 

https://github.com/gorakhargosh/mom

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import sys
import types
import struct

PY3 = sys.version_info[0] == 3

if PY3: # pragma: no cover
	string_types = str,
	integer_types = int,
	class_types = type,
	text_type = str
	binary_type = bytes
else:
	string_types = basestring,
	integer_types = (int, long)
	class_types = (type, types.ClassType)
	text_type = unicode
	binary_type = str

try:
	INT_MAX = sys.maxsize
except AttributeError:
	INT_MAX = sys.maxint

INT64_MAX = (1 << 63) - 1
INT32_MAX = (1 << 31) - 1
INT16_MAX = (1 << 15) - 1
UINT128_MAX = (1 << 128) - 1		# 340282366920938463463374607431768211455L
UINT64_MAX = 0xffffffffffffffff		# ((1 << 64) - 1)
UINT32_MAX = 0xffffffff				# ((1 << 32) - 1)
UINT16_MAX = 0xffff					# ((1 << 16) - 1)
UINT8_MAX = 0xff

# Determine the word size of the processor.
if INT_MAX == INT64_MAX:
	# 64-bit processor.
	MACHINE_WORD_SIZE = 64
	UINT_MAX = UINT64_MAX
elif INT_MAX == INT32_MAX:
	# 32-bit processor.
	MACHINE_WORD_SIZE = 32
	UINT_MAX = UINT32_MAX
else:
	MACHINE_WORD_SIZE = 64
	UINT_MAX = UINT64_MAX

try:
	LONG_TYPE = long
except NameError:
	LONG_TYPE = int

try:
	INT_TYPE = long
	INTEGER_TYPES = (int, long)
except NameError:
	INT_TYPE = int
	INTEGER_TYPES = (int,)

try:
	BYTES_TYPE = bytes
except NameError:
	BYTES_TYPE = str

try:
	HAVE_PYTHON3 = False
	UNICODE_TYPE = unicode
	BASESTRING_TYPE = basestring

	def byte_ord(byte_):
		"""
		Returns the ordinal value of the given byte.

		:param byte_: 
			The byte.
		:returns:
			Integer representing ordinal value of the byte.
		"""
		return ord(byte_)
except NameError:
	def byte_ord(byte_):
		"""
		Returns the ordinal value of the given byte.

		:param byte_:
			The byte.
		:returns:
			Integer representing ordinal value of the byte.
		"""
		return byte_

	UNICODE_TYPE = str
	HAVE_PYTHON3 = True
	BASESTRING_TYPE = (str, bytes)

# Fake byte literals for python2.5
if str is UNICODE_TYPE:
	def byte_literal(literal):
		return literal.encode("latin1")
else:
	def byte_literal(literal):
		return literal

EMPTY_BYTE = byte_literal("")
EQUAL_BYTE = byte_literal("=")
PLUS_BYTE = byte_literal("+")
HYPHEN_BYTE = byte_literal("-")
ZERO_BYTE = byte_literal("\x00")
UNDERSCORE_BYTE = byte_literal("_")
DIGIT_ZERO_BYTE = byte_literal("0")
FORWARD_SLASH_BYTE = byte_literal("/")
HAVE_LITTLE_ENDIAN = bool(struct.pack(b"h", 1) == "\x01\x00")

if getattr(dict, "iteritems", None):
	def dict_each(func, iterable):
		"""
		Portably iterate through a dictionary's items.
	
		:param func:
			The function that will receive two arguments: key, value.
		:param iterable:
			The dictionary iterable.
		"""
		for key, value in iterable.iteritems():
			func(key, value)
else:
	def dict_each(func, iterable):
		"""
		Portably iterate through a dictionary's items.
	
		:param func:
			The function that will receive two arguments: key, value.
		:param iterable:
			The dictionary iterable.
		"""
		for key, value in iterable.items():
			func(key, value)

def get_word_alignment(num, force_arch=64,
					   _machine_word_size=MACHINE_WORD_SIZE):
	"""
	Returns alignment details for the given number based on the platform
	Python is running on.
	
	:param num:
	  Unsigned integral number.
	:param force_arch:
	  If you don't want to use 64-bit unsigned chunks, set this to
	  anything other than 64. 32-bit chunks will be preferred then.
	  Default 64 will be used when on a 64-bit machine.
	:param _machine_word_size:
	  (Internal) The machine word size used for alignment.
	:returns:
	  4-tuple::
	
		  (word_bits, word_bytes,
		   max_uint, packing_format_type)
	"""
	if force_arch == 64 and _machine_word_size >= 64 and num > UINT32_MAX:
		# 64-bit unsigned integer.
		return 64, 8, UINT64_MAX, "Q"
	elif num > UINT16_MAX:
		# 32-bit unsigned integer
		return 32, 4, UINT32_MAX, "L"
	elif num > UINT8_MAX:
		# 16-bit unsigned integer.
		return 16, 2, UINT16_MAX, "H"
	else:
		# 8-bit unsigned integer.
		return 8, 1, UINT8_MAX, "B"

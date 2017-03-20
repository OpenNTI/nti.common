#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deals with a lot of cross-version issues.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

# Taken from https://github.com/gorakhargosh/mom

import six
import sys
import struct

PY3 = sys.version_info[0] == 3

text_type = six.text_type
binary_type = six.binary_type
class_types = six.class_types
string_types = six.string_types
integer_types = six.integer_types


if PY3:  # pragma: no cover
    _unicode = lambda x: x

    def native_(s, encoding='utf-8', errors='strict'):
        """
        If ``s`` is an instance of ``text_type``, return
        ``s``, otherwise return ``str(s, encoding, errors)``
        """
        if isinstance(s, text_type):
            return s
        return str(s, encoding, errors)

else:
    _unicode = unicode

    def native_(s, encoding='utf-8', errors='strict'):
        """
        If ``s`` is an instance of ``text_type``, return
        ``s.encode(encoding, errors)``, otherwise return ``str(s)``
        """
        if isinstance(s, text_type):
            return s.encode(encoding, errors)
        return str(s)


def unicode_(s, encoding='utf-8', err='strict'):
    """
    Decode a byte sequence and unicode result
    """
    s = s.decode(encoding, err) if isinstance(s, bytes) else s
    return _unicode(s) if s is not None else None
safestr = to_unicode = unicode_  # BWC


try:
    INT_MAX = sys.maxsize
except AttributeError:
    INT_MAX = sys.maxint

INT64_MAX = six.MAXSIZE
INT32_MAX = (1 << 31) - 1
INT16_MAX = (1 << 15) - 1
UINT128_MAX = (1 << 128) - 1  # 340282366920938463463374607431768211455L

UINT8_MAX = 0xff
UINT16_MAX = 0xffff  # ((1 << 16) - 1)
UINT32_MAX = 0xffffffff  # ((1 << 32) - 1)
UINT64_MAX = 0xffffffffffffffff  # ((1 << 64) - 1)

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
except NameError:
    INT_TYPE = int
INTEGER_TYPES = six.integer_types

BYTES_TYPE = six.binary_type

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


def get_word_alignment(num, force_arch=64, _machine_word_size=MACHINE_WORD_SIZE):
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

word_alignment = get_word_alignment

# python3/pypy compatibility shims.

from zope import interface

try:
    from Acquisition.interfaces import IAcquirer
except ImportError:
    class IAcquirer(interface.Interface):
        pass

try:
    from Acquisition import Implicit
except ImportError:
    @interface.implementer(IAcquirer)
    class Implicit(object):
        pass
Implicit = Implicit

try:
    from ExtensionClass import Base
except ImportError:
    class Base(object):
        pass
Base = Base  # pylint

try:
    from Acquisition import aq_base
except ImportError:
    def aq_base(o):
        return o
aq_base = aq_base

try:
    from gevent import sleep
    from gevent import Greenlet
    from gevent.queue import Queue
except ImportError:
    from Queue import Queue
    try:
        from greenlet import greenlet as Greenlet
    except ImportError:
        class Greenlet(object):
            pass
    from time import sleep

slee = sleep
Queue = Queue
Greenlet = Greenlet

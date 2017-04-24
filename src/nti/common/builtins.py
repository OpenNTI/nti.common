#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Taken from https://github.com/gorakhargosh/mom

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import struct

from nti.common import _compat


def byte(number):
    """
    Converts a number between 0 and 255 (both inclusive) to a base-256 (byte)
    representation.

    Use it as a replacement for ``chr`` where you are expecting a byte
    because this will work on all versions of Python.

    Raises :class:``struct.error`` on overflow.

    :param number:
            An unsigned integer between 0 and 255 (both inclusive).
    :returns:
            A single byte.
    """
    return struct.pack(b"B", number)


def bytes_leading(raw_bytes, needle=_compat.ZERO_BYTE):
    """
    Finds the number of prefixed byte occurrences in the haystack.

    Useful when you want to deal with padding.

    :param raw_bytes:
            Raw bytes.
    :param needle:
            The byte to count. Default \000.
    :returns:
            The number of leading needle bytes.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("argument must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    leading = 0
    # Indexing keeps compatibility between Python 2.x and Python 3.x
    needle_byte = needle[0]
    for raw_byte in raw_bytes:
        if raw_byte == needle_byte:
            leading += 1
        else:
            break
    return leading


def bin_(number, prefix="0b"):
    """
    Converts a long value to its binary representation.

    :param number:
            Long value.
    :param prefix:
            The prefix to use for the bitstring. Default "0b" to mimic Python
            builtin ``bin()``.
    :returns:
            Bit string.
    """
    if number is None:
        raise TypeError("'%r' object cannot be interpreted as an index" %
                        type(number).__name__)
    prefix = prefix or ""
    if number < 0:
        number = -number
        prefix = "-" + prefix
    bit_string = ""
    while number > 1:
        bit_string = str(number & 1) + bit_string
        number >>= 1
    bit_string = str(number) + bit_string
    return prefix + bit_string


def hex_(number, prefix="0x"):
    """
    Converts a integer value to its hexadecimal representation.

    :param number:
            Integer value.
    :param prefix:
            The prefix to use for the hexadecimal string. Default "0x" to mimic
            ``hex()``.
    :returns:
            Hexadecimal string.
    """
    prefix = prefix or ""
    if number < 0:
        number = -number
        prefix = "-" + prefix
    # Make sure this is an int and not float.
    _ = number & 1
    hex_num = "%x" % number
    return prefix + hex_num.lower()


def is_unicode(obj):
    """
    Determines whether the given value is a Unicode string.

    :param obj:
            The value to test.
    :returns:
            ``True`` if value is a Unicode string; ``False`` otherwise.
    """
    return isinstance(obj, _compat.UNICODE_TYPE)


def is_bytes(obj):
    """
    Determines whether the given value is a bytes instance.

    :param obj:
            The value to test.
    :returns:
            ``True`` if value is a bytes instance; ``False`` otherwise.
    """
    return isinstance(obj, _compat.BYTES_TYPE)


def is_bytes_or_unicode(obj):
    """
    Determines whether the given value is an instance of a string irrespective
    of whether it is a byte string or a Unicode string.

    :param obj:
            The value to test.
    :returns:
            ``True`` if value is any type of string; ``False`` otherwise.
    """
    return isinstance(obj, _compat.BASESTRING_TYPE)


def is_integer(obj):
    """
    Determines whether the object value is actually an integer and not a bool.

    :param obj:
            The value to test.
    :returns:
            ``True`` if yes; ``False`` otherwise.
    """
    return isinstance(obj, _compat.INTEGER_TYPES) and not isinstance(obj, bool)


def integer_byte_length(number):
    """
    Number of bytes needed to represent a integer excluding any prefix 0 bytes.

    :param number:
            Integer value. If num is 0, returns 0.
    :returns:
            The number of bytes in the integer.
    """
    quanta, remainder = divmod(integer_bit_length(number), 8)
    if remainder:
        quanta += 1
    return quanta


def integer_bit_length(number):
    """
    Number of bits needed to represent a integer excluding any prefix
    0 bits.

    :param number:
            Integer value. If num is 0, returns 0. Only the absolute value of the
            number is considered. Therefore, signed integers will be abs(num)
            before the number's bit length is determined.
    :returns:
            Returns the number of bits in the integer.
    """
    # Public domain. Taken from tlslite. This is the fastest implementation
    # I have found.

    # Do not change this to `not num` otherwise a TypeError will not
    # be raised when `None` is passed in as a value.
    if number == 0:
        return 0
    if number < 0:
        number = -number
        # Make sure this is an int and not float.
    _ = number & 1
    hex_num = "%x" % number
    return ((len(hex_num) - 1) * 4) + {
        "0": 0, "1": 1, "2": 2, "3": 2,
        "4": 3, "5": 3, "6": 3, "7": 3,
        "8": 4, "9": 4, "a": 4, "b": 4,
        "c": 4, "d": 4, "e": 4, "f": 4,
    }[hex_num[0]]


def integer_bit_size(number):
    """
    Number of bits needed to represent a integer excluding any prefix
    0 bits.

    :param number:
            Integer value. If num is 0, returns 1. Only the absolute value of the
            number is considered. Therefore, signed integers will be abs(num)
            before the number's bit length is determined.
    :returns:
            Returns the number of bits in the integer.
    """
    if number == 0:
        return 1
    return integer_bit_length(number)


def integer_bit_count(number):
    """
    Returns the number of set (1) bits in an unsigned integer.

    :param number:
            An integer. If this is a negative integer, its absolute
            value will be considered.
    :returns:
            The number of set bits in an unsigned integer.
    """
    # Licensed under the PSF License.
    # Taken from http://wiki.python.org/moin/BitManipulation
    number = abs(number)
    count = 0
    while number:
        number &= number - 1
        count += 1
    return count

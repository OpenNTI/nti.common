#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Taken from https://github.com/gorakhargosh/mom

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six
import struct


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
    return struct.pack("B", number)


def is_integer(obj):
    """
    Determines whether the object value is actually an integer and not a bool.

    :param obj:
            The value to test.
    :returns:
            ``True`` if yes; ``False`` otherwise.
    """
    return isinstance(obj, six.integer_types) and not isinstance(obj, bool)


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

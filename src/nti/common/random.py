#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import math

from nti.common import codec
from nti.common import string
from nti.common import integer
from nti.common import builtins

ALPHA = string.ASCII_LETTERS
ALPHANUMERIC = ALPHA + string.DIGITS

UPPERCASE_ALPHA = string.ASCII_UPPERCASE
UPPERCASE_ALPHANUMERIC = UPPERCASE_ALPHA + string.DIGITS

ASCII_PRINTABLE = ALPHA + string.DIGITS + string.PUNCTUATION

LOG_OF_2 = 0.6931471805599453

# INIT
os.urandom(1)


def generate_random_bytes(count):
    """
    Generates a random byte string with ``count`` bytes.

    :param count:
            Number of bytes.
    :returns:
            Random byte string.
    """
    return os.urandom(count)


def generate_random_bits(n_bits, rand_func=generate_random_bytes):
    """
    Generates the specified number of random bits as a byte string.
    For example::

            f(x) -> y such that
            f(16) ->           1111 1111 1111 1111; bytes_to_integer(y) => 65535L
            f(17) -> 0000 0001 1111 1111 1111 1111; bytes_to_integer(y) => 131071L

    :param n_bits: Number of random bits.

      if n is divisible by 8, (n / 8) bytes will be returned.
      if n is not divisible by 8, ((n / 8) + 1) bytes will be returned
      and the prefixed offset-byte will have `(n % 8)` number of random bits,
      (that is, `8 - (n % 8)` high bits will be cleared).

      The range of the numbers is 0 to (2**n)-1 inclusive.
    :param rand_func: Random bytes generator function.
    :returns: Bytes.
    """
    if not builtins.is_integer(n_bits):
        raise TypeError("unsupported operand type: %r" % type(n_bits).__name__)
    if n_bits <= 0:
        raise ValueError("number of bits must be greater than 0.")
    # Doesn't perform any floating-point operations.
    quotient, remainder = divmod(n_bits, 8)
    random_bytes = rand_func(quotient)
    if remainder:
        offset = ord(rand_func(1)) >> (8 - remainder)
        random_bytes = builtins.byte(offset) + random_bytes
    return random_bytes


def generate_random_uint_atmost(n_bits, rand_func=generate_random_bytes):
    """
    Generates a random unsigned integer with `n_bits` random bits.

    :param n_bits:
      Number of random bits to be generated at most.
    :param rand_func:
      Random bytes generator function.
    :returns:
      Returns an unsigned long integer with at most `n_bits` random bits.
      The generated unsigned long integer will be between 0 and
      (2**n_bits)-1 both inclusive.
    """
    if not builtins.is_integer(n_bits):
        raise TypeError("unsupported operand type: %r" % type(n_bits).__name__)
    if n_bits <= 0:
        raise ValueError("number of bits must be greater than 0.")
        # Doesn't perform any floating-point operations.
    quotient, remainder = divmod(n_bits, 8)
    if remainder:
        quotient += 1
    random_bytes = rand_func(quotient)
    mask = (1 << n_bits) - 1
    return mask & integer.bytes_to_uint(random_bytes)


def generate_random_uint_between(low, high, rand_func=generate_random_bytes):
    """
    Generates a random long integer between low and high, not including high.

    :param low:
      Low
    :param high:
      High
    :param rand_func:
      Random bytes generator function.
    :returns:
      Random unsigned long integer value.
    """
    if not (builtins.is_integer(low) and builtins.is_integer(high)):
        raise TypeError("unsupported argument types(s): %r and %r" %
                        (type(low).__name__, type(high).__name__))
    if low >= high:
        raise ValueError("high value must be greater than low value.")
    substrate = high - low - 1
    bits = builtins.integer_bit_size(substrate)
    value = generate_random_uint_atmost(bits, rand_func=rand_func)
    while value > substrate:
        value = generate_random_uint_atmost(bits, rand_func=rand_func)
    return low + value


def generate_random_hex_string(length=8, rand_func=generate_random_bytes):
    """
    Generates a random ASCII-encoded hexadecimal string of an even length.

    :param length:
            Length of the string to be returned. Default 32.
            The length MUST be a positive even number.
    :param rand_func:
            Random bytes generator function.
    :returns:
            A string representation of a randomly-generated hexadecimal string.
    """
    # if length % 2 or length <= 0:
    if length & 1 or length <= 0:
        raise ValueError("This function expects a positive even number "
                         "length: got length `%r`." % length)
    result = codec.hex_encode(rand_func(length >> 1))
    return result


def random_choice(sequence, rand_func=generate_random_bytes):
    """
    Randomly chooses an element from the given non-empty sequence.

    :param sequence:
            Non-empty sequence to randomly choose an element from.
    :returns:
            Randomly chosen element.
    """
    return sequence[generate_random_uint_between(0, len(sequence), rand_func)]


def generate_random_sequence(length, pool, rand_func=generate_random_bytes):
    """
    Generates a random sequence of given length using the sequence
    pool specified.

    :param length:
            The length of the random sequence.
    :param pool:
            A sequence of elements to be used as the pool from which
            random elements will be chosen.
    :returns:
            A list of elements randomly chosen from the pool.
    """
    if not builtins.is_integer(length):
        raise TypeError("Length must be a positive integer: got `%r`" %
                        type(length).__name__)
    if length <= 0:
        raise ValueError("length must be a positive integer: got %d" % length)
    return [random_choice(pool, rand_func) for _ in range(length)]


def generate_random_string(length=10, pool=ALPHANUMERIC,
                           rand_func=generate_random_bytes):
    """
    Generates a random string of given length using the sequence
    pool specified.

    Don't use this to generate passwords. Use generate_random_password instead.

    Entropy:

             H = log2(N**L)

    where:

    * H is the entropy in bits.
    * N is the possible symbol count
    * L is length of string of symbols

    Entropy chart::

            -----------------------------------------------------------------
            Symbol set              Symbol Count (N)  Entropy per symbol (H)
            -----------------------------------------------------------------
            HEXADECIMAL_DIGITS        16              4.0000 bits
            DIGITS                    10              3.3219 bits
            LOWERCASE_ALPHA           26              4.7004 bits
            UPPERCASE_ALPHA           26              4.7004 bits
            PUNCTUATION               32              5.0000 bits
            LOWERCASE_ALPHANUMERIC    36              5.1699 bits
            UPPERCASE_ALPHANUMERIC    36              5.1699 bits
            ALPHA                     52              5.7004 bits
            ALPHANUMERIC              62              5.9542 bits
            ASCII_PRINTABLE           94              6.5546 bits
            ALL_PRINTABLE             100             6.6438 bits

    :param length:
            The length of the random sequence.
    :param pool:
            A sequence of characters to be used as the pool from which
            random characters will be chosen. Default case-sensitive alpha-numeric
            characters.
    :returns:
            A string of elements randomly chosen from the pool.
    """
    result = "".join(generate_random_sequence(length, pool, rand_func))
    return result


def generate_random_sequence_strong(entropy=64, pool=ASCII_PRINTABLE,
                                    rand_func=generate_random_bytes):
    """
    Generates a random sequence based on entropy.

    If you're using this to generate passwords based on entropy:
    http://en.wikipedia.org/wiki/Password_strength

    :param entropy:
            Desired entropy in bits.
    :param pool:
            The pool of unique elements from which to randomly choose.
    :returns:
            Randomly generated sequence with specified entropy.
    """
    pool = list(set(pool))
    length = int(math.ceil((LOG_OF_2 / math.log(len(pool))) * entropy))
    return generate_random_sequence(length, pool, rand_func)


def generate_random_password(entropy=64, pool=ASCII_PRINTABLE,
                             rand_func=generate_random_bytes):
    """
    Generates a password based on entropy.

    If you're using this to generate passwords based on entropy:
    http://en.wikipedia.org/wiki/Password_strength

    :param entropy:
            Desired entropy in bits. Choose at least 64 to have a decent password.
    :param pool:
            The pool of unique characters from which to randomly choose.
    :returns:
            Randomly generated password with specified entropy.
    """
    result = "".join(generate_random_sequence_strong(entropy, pool, rand_func))
    return result

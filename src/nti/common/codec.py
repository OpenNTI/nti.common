#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import binascii

from nti.common import builtins


def hex_encode(raw_bytes):
    """
    Encodes raw bytes into hexadecimal representation.

    Encode your Unicode strings to a byte encoding before hex-encoding them.

    :param raw_bytes:
            Bytes.
    :returns:
            Hex-encoded representation.
    """
    if not builtins.is_bytes(raw_bytes):
        raise TypeError("argument must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    result = binascii.b2a_hex(raw_bytes)
    return result


def base64_encode(raw_bytes):
    """
    Encodes raw bytes into base64 representation without appending a trailing
    newline character. Not URL-safe.

    Encode your Unicode strings to a byte encoding before base64-encoding them.

    :param raw_bytes:
            Bytes to encode.
    :returns:
            Base64 encoded bytes without newline characters.
    """
    if not builtins.is_bytes(raw_bytes):
        raise TypeError("argument must be bytes: got %r" %
                        type(raw_bytes).__name__)
    return binascii.b2a_base64(raw_bytes)[:-1]

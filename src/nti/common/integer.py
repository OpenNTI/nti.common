#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six
import binascii


def bytes_to_uint(raw_bytes):
    """
    Converts a series of bytes into an unsigned integer.

    :param raw_bytes:
            Raw bytes (base-256 representation).

    :returns:
            Unsigned integer.
    """
    if not isinstance(raw_bytes, six.binary_type):
        raise TypeError("raw_bytes must be native string: got %r" %
                        type(raw_bytes).__name__)
    # binascii.b2a_hex is written in C as is int.
    return int(binascii.b2a_hex(raw_bytes), 16)

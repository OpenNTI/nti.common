#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import binascii

from nti.common._compat import bytes_


def hex_encode(raw_bytes):
    """
    Encodes raw bytes into hexadecimal representation.
    """
    return binascii.b2a_hex(bytes_(raw_bytes))


def base64_encode(raw_bytes):
    """
    Encodes raw bytes into base64 representation without appending a trailing
    newline character. Not URL-safe.
    """
    return binascii.b2a_base64(bytes_(raw_bytes))[:-1]

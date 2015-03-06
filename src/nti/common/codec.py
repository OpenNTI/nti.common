#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import binascii

from . import builtins

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

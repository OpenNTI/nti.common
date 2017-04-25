#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six
import hmac
import hashlib

from nti.common.codec import hex_encode
from nti.common.codec import base64_encode


def sha1_digest(*inputs):
    """
    Calculates a SHA-1 digest of a variable number of inputs.

    :param inputs:
            A variable number of inputs for which the digest will be calculated.
    :returns:
            A byte string containing the SHA-1 message digest.
    """
    hash_func = hashlib.sha1()
    for i in inputs:
        if not isinstance(i, six.binary_type):
            raise TypeError("input must be native string: got %r" %
                            type(i).__name__)
        hash_func.update(i)
    return hash_func.digest()


def sha1_hex_digest(*inputs):
    """
    Calculates hexadecimal representation of the SHA-1 digest of a variable
    number of inputs.

    :param inputs:
            A variable number of inputs for which the digest will be calculated.
    :returns:
            Hexadecimal representation of the SHA-1 digest.
    """
    return hex_encode(sha1_digest(*inputs))


def sha1_base64_digest(*inputs):
    """
    Calculates Base-64-encoded SHA-1 digest of a variable
    number of inputs.

    :param inputs:
            A variable number of inputs for which the digest will be calculated.
    :returns:
            Base-64-encoded SHA-1 digest.
    """
    return base64_encode(sha1_digest(*inputs))


def md5_digest(*inputs):
    """
    Calculates a MD5 digest of a variable number of inputs.

    :param inputs:
            A variable number of inputs for which the digest will be calculated.
    :returns:
            A byte string containing the MD5 message digest.
    """
    hash_func = hashlib.md5()
    for i in inputs:
        if not isinstance(i, six.binary_type):
            raise TypeError("input must be native string: got %r" %
                            type(i).__name__)
        hash_func.update(i)
    return hash_func.digest()


def md5_hex_digest(*inputs):
    """
    Calculates hexadecimal representation of the MD5 digest of a variable
    number of inputs.

    :param inputs:
            A variable number of inputs for which the digest will be calculated.
    :returns:
            Hexadecimal representation of the MD5 digest.
    """
    return hex_encode(md5_digest(*inputs))


def md5_base64_digest(*inputs):
    """
    Calculates Base-64-encoded MD5 digest of a variable
    number of inputs.

    :param inputs:
            A variable number of inputs for which the digest will be calculated.
    :returns:
            Base-64-encoded MD5 digest.
    """
    return base64_encode(md5_digest(*inputs))


def hmac_sha1_digest(key, data):
    """
    Calculates a HMAC SHA-1 digest.

    :param key:
            The key for the digest.
    :param data:
            The raw bytes data for which the digest will be calculated.
    :returns:
            HMAC SHA-1 Digest.
    """
    if not isinstance(data, six.binary_type):
        raise TypeError("data must be native string: got %r" %
                        type(data).__name__)
    return hmac.new(key, data, hashlib.sha1).digest()


def hmac_sha1_base64_digest(key, data):
    """
    Calculates a base64-encoded HMAC SHA-1 signature.

    :param key:
            The key for the signature.
    :param data:
            The data to be signed.
    :returns:
            Base64-encoded HMAC SHA-1 signature.
    """
    return base64_encode(hmac_sha1_digest(key, data))

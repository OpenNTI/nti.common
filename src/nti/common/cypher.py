#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six
import base64
from itertools import cycle

from nti.common._compat import text_
from nti.common._compat import bytes_

logger = __import__('logging').getLogger(__name__)


if six.PY3:
    def _ord(x): return x
    def _convert(x): return bytes_(x)
else:
    _ord = ord
    def _convert(x): return x


def is_base64(s):
    try:
        return text_(base64.b64encode(_convert(base64.b64decode(s)))) == text_(s)
    except Exception:
        pass
    return False


def _XOR(text, key):
    """
    A TOY "cipher" that symmetrically obscures
    the `text` based `key`. Do not use this when
    security matters.
    """
    result = []
    key = cycle(_convert(key))
    for t in _convert(text):
        t = chr(_ord(t) ^ _ord(next(key)))
        result.append(t)
    result = u''.join(result)
    return result


DEFAULT_PASSPHRASE = base64.b64decode('TjN4dFRoMHVnaHQhIUM=')


def make_ciphertext(plaintext, passphrase=DEFAULT_PASSPHRASE):
    """
    A trivial function that uses a toy "cipher" (XOR) to obscure
    and then base64 encode a sequence of bytes.
    """
    encoded = _XOR(plaintext, passphrase)
    result = base64.b64encode(_convert(encoded))
    return result


def get_plaintext(ciphertext, passphrase=DEFAULT_PASSPHRASE):
    """
    A trivial function that uses a toy "cipher" (XOR) to obscure
    a base64 encoded sequence of bytes.
    """
    result = base64.b64decode(ciphertext)
    result = _XOR(result, passphrase)
    return result

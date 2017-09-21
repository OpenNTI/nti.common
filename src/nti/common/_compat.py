#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deals with a lot of cross-version issues.

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six

import zope.deferredimport

from zope import interface

if six.PY3:  # pragma: no cover
    def _unicode(s): return str(s)
else:
    _unicode = unicode


def text_(s, encoding='utf-8', err='strict'):
    """
    Decode a byte sequence and unicode result
    """
    s = s.decode(encoding, err) if isinstance(s, bytes) else s
    return _unicode(s) if s is not None else None


def bytes_(s, encoding='utf-8', errors='strict'):
    """
    If ``s`` is an instance of ``text_type``, return
    ``s.encode(encoding, errors)``, otherwise return ``s``
    """
    if isinstance(s, six.text_type):
        return s.encode(encoding, errors)
    return s


try:
    UNICODE_TYPE = unicode
    BASESTRING_TYPE = basestring
except NameError:
    UNICODE_TYPE = str
    BASESTRING_TYPE = (str, bytes)

# Fake byte literals for python2.5
if str is UNICODE_TYPE:
    def byte_literal(literal):
        return literal.encode("latin1")
else:
    def byte_literal(literal):
        return literal

ZERO_BYTE = byte_literal("\x00")
DIGIT_ZERO_BYTE = byte_literal("0")


# Deprecations

zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Import from nti.base._compat instead",
    safestr='nti.base._compat:text_',
    unicode_='nti.base._compat:text_',
    to_unicode='nti.base._compat:text_',)

zope.deferredimport.deprecated(
    "Import from nti.base._compat instead",
    native_='nti.base._compat:native_',)


# BWC

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
    try:
        from Queue import Queue
    except ImportError:
        from asyncio import Queue
    try:
        from greenlet import greenlet as Greenlet
    except ImportError:
        class Greenlet(object):
            pass
    from time import sleep

slee = sleep
Queue = Queue
Greenlet = Greenlet

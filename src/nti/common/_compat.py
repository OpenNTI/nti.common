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

from zope import interface
from zope import deferredimport


def text_(s, encoding='utf-8', err='strict'):
    """
    Decode a byte sequence and unicode result
    """
    if not isinstance(s, six.text_type) and s is not None:
        s = s.decode(encoding, err)
    return s


def bytes_(s, encoding='utf-8', errors='strict'):
    """
    If ``s`` is an instance of ``text_type``, return
    ``s.encode(encoding, errors)``, otherwise return ``s``
    """
    if not isinstance(s, bytes) and s is not None:
        return s.encode(encoding, errors)
    return s


# BWC


try:
    from Acquisition.interfaces import IAcquirer
except ImportError:   # pragma: no cover
    class IAcquirer(interface.Interface):
        pass

try:
    from Acquisition import Implicit
except ImportError:  # pragma: no cover
    @interface.implementer(IAcquirer)
    class Implicit(object):
        pass
Implicit = Implicit

try:
    from ExtensionClass import Base
except ImportError:  # pragma: no cover
    class Base(object):
        pass
Base = Base  # pylint

try:
    from Acquisition import aq_base
except ImportError:  # pragma: no cover
    def aq_base(o):
        return o
aq_base = aq_base

try:
    from gevent import sleep
except ImportError:  # pragma: no cover
    from time import sleep
sleep = sleep

try:
    from gevent import Greenlet
except ImportError:  # pragma: no cover
    try:
        from greenlet import greenlet as Greenlet
    except ImportError:
        class Greenlet(object):
            pass
Greenlet = Greenlet

try:
    from gevent.queue import Queue
except ImportError:  # pragma: no cover
    try:
        from Queue import Queue
    except ImportError:
        from asyncio import Queue
Queue = Queue


# Deprecations


deferredimport.initialize()
deferredimport.deprecated(
    "Import from nti.base._compat instead",
    safestr='nti.base._compat:text_',
    unicode_='nti.base._compat:text_',
    to_unicode='nti.base._compat:text_',)

deferredimport.deprecated(
    "Import from nti.base._compat instead",
    native_='nti.base._compat:native_',)

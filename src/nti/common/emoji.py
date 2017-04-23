#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from emoji import demojize


def has_emoji_chars(s):
    if isinstance(s, bytes):
        s = s.decode("utf-8")
    return demojize(s) != s
has_emoji = has_emoji_chars  # BWC

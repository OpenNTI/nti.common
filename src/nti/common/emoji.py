#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from emoji import demojize

from nti.common.string import unicode_


def has_emoji_chars(s):
    source = unicode_(s)
    return demojize(source) != source
has_emoji = has_emoji_chars  # BWC

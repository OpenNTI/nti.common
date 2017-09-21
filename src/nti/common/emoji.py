#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from emoji import demojize


def has_emoji_chars(s):
    if isinstance(s, bytes):
        s = s.decode("utf-8")
    return demojize(s) != s
has_emoji = has_emoji_chars  # BWC

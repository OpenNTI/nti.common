#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import has_length
from hamcrest import assert_that

import unittest

from nti.common.string import emoji_ranges
        
class TestString(unittest.TestCase):
    
    def test_emoji_ranges(self):
        ranges = emoji_ranges()
        assert_that(ranges, has_length(722))

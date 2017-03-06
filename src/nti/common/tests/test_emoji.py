#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that

import unittest

from nti.common.emoji import emoji_chars
from nti.common.emoji import has_emoji_chars


class TestString(unittest.TestCase):

    def test_emoji_chars(self):
        ranges = emoji_chars()
        assert_that(ranges, has_length(722))

    def test_has_emoji(self):
        assert_that(has_emoji_chars(u"ichigo"), is_(False))
        assert_that(has_emoji_chars(u"ichigo #"), is_(False))
        assert_that(has_emoji_chars(u'ichigo \U0001f383'), is_(True))
        assert_that(has_emoji_chars(b'San\xf0\x9f\x98\x81chez'), is_(True))
        assert_that(has_emoji_chars(b'ichigo \xf0\x9f\x8e\x83'), is_(True))

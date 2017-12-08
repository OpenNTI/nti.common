#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that

import unittest

from nti.common.emoji import has_emoji_chars


class TestEmoji(unittest.TestCase):

    def test_has_emoji(self):
        assert_that(has_emoji_chars(u"ichigo"), is_(False))
        assert_that(has_emoji_chars(u"ichigo #"), is_(False))
        assert_that(has_emoji_chars(u'ichigo \U0001f383'), is_(True))
        assert_that(has_emoji_chars(b'San\xf0\x9f\x98\x81chez'), is_(True))
        assert_that(has_emoji_chars(b'ichigo \xf0\x9f\x8e\x83'), is_(True))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_property

import unittest

from nti.common.model import OAuthKeys


class TestModel(unittest.TestCase):

    def test_oauthkeys(self):
        m = OAuthKeys()
        m.secretKey = u'L7oCETo='
        assert_that(m, has_property('secretKey', is_('L7oCETo=')))

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
from nti.common.model import PersistentOAuthKeys


class TestModel(unittest.TestCase):

    def test_oauthkeys(self):
        m = OAuthKeys()
        m.secretKey = u'L7oCETo='
        assert_that(m, has_property('secretKey', is_('L7oCETo=')))

    def test_persitent_oauthkeys(self):
        m = PersistentOAuthKeys()
        m.secretKey = u'L7oCETo='
        m.apiKey = u'test-api-key'
        assert_that(m, has_property('secretKey', is_('L7oCETo=')))
        assert_that(m, has_property('apiKey', is_('test-api-key')))

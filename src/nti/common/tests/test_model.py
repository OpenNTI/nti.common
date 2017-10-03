#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_property

import unittest

from nti.common.model import LDAP
from nti.common.model import OAuthKeys


class TestModel(unittest.TestCase):

    def test_ldap(self):
        m = LDAP()
        m.password = u'L7oCETo='  # base64; bad cypher text
        assert_that(m, has_property('password', is_('L7oCETo=')))

    def test_oauthkeys(self):
        m = OAuthKeys()
        m.secretKey = u'L7oCETo='  # base64; bad cypher text
        assert_that(m, has_property('secretKey', is_('L7oCETo=')))

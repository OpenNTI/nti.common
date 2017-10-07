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

import fudge
import unittest

from nti.common.model import OAuthKeys


class TestModel(unittest.TestCase):

    @fudge.patch('nti.common.model.is_base64',
                 'nti.common.model.get_plaintext')
    def test_oauthkeys(self, mock_ib64, mock_gpt):
        mock_ib64.is_callable().with_args().returns(True)
        mock_gpt.is_callable().with_args().raises(TypeError())
        m = OAuthKeys()
        m.secretKey = u'L7oCETo='  # base64; bad cypher text
        assert_that(m, has_property('secretKey', is_('L7oCETo=')))

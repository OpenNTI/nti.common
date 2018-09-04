#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

import unittest

from hamcrest import is_
from hamcrest import assert_that

from nti.common.url import safe_add_query_params


class TestURL(unittest.TestCase):

    def test_safe_add_query_params(self):
        # Test basic add params
        test_url = 'http://alpha.dev:8082/dataserver2'
        params = {'test': 'encode'}
        new_url = safe_add_query_params(test_url, params)
        assert_that(new_url,
                    is_('http://alpha.dev:8082/dataserver2?test=encode'))

        # Test add params to existing query
        test_url = 'http://alpha.dev:8082/dataserver2?error=none'
        params = {'test': 'encode'}
        new_url = safe_add_query_params(test_url, params)
        assert_that(new_url,
                    is_('http://alpha.dev:8082/dataserver2?error=none&test=encode'))

        # Test percent encoded spaces
        test_url = 'http://alpha.dev:8082/dataserver2'
        params = {'test': 'encode space'}
        new_url = safe_add_query_params(test_url, params)
        assert_that(new_url,
                    is_('http://alpha.dev:8082/dataserver2?test=encode+space'))

        # Test percent encoded spaces to existing params
        test_url = 'http://alpha.dev:8082/dataserver2?error=no+error'
        params = {'test': 'encode space'}
        new_url = safe_add_query_params(test_url, params)
        assert_that(new_url,
                    is_('http://alpha.dev:8082/dataserver2?error=no+error&test=encode+space'))

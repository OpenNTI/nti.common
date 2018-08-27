#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import unittest

from hamcrest import assert_that
from hamcrest import is_

from nti.common.url import safe_add_query_params

logger = __import__('logging').getLogger(__name__)


class TestUrl(unittest.TestCase):

    def test_safe_add_query_params(self):

        from IPython.terminal.debugger import set_trace;set_trace()

        # Test basic add params
        test_url = 'http://alpha.dev:8082/dataserver2'
        params = {'test': 'encode'}
        new_url = safe_add_query_params(test_url, params)
        assert_that(new_url, is_('http://alpha.dev:8082/dataserver2?test=encode'))

        # Test add params to existing query
        test_url = 'http://alpha.dev:8082/dataserver2?error=none'
        params = {'test': 'encode'}
        new_url = safe_add_query_params(test_url, params)
        assert_that(new_url, is_('http://alpha.dev:8082/dataserver2?test=encode&error=none'))

        # Test percent encoded spaces
        test_url = 'http://alpha.dev:8082/dataserver2'
        params = {'test': 'encode space'}
        new_url = safe_add_query_params(test_url, params)
        assert_that(new_url, is_('http://alpha.dev:8082/dataserver2?test=encode%20space'))

        # Test percent encoded spaces to existing params
        test_url = 'http://alpha.dev:8082/dataserver2?error=no+error'
        params = {'test': 'encode space'}
        new_url = safe_add_query_params(test_url, params)
        assert_that(new_url, is_('http://alpha.dev:8082/dataserver2?test=encode%20space&error=no%20error'))

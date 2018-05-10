#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that

import unittest

from nti.common.string import TRUE_VALUES
from nti.common.string import FALSE_VALUES

from nti.common.string import is_true
from nti.common.string import is_false
from nti.common.string import equals_ignore_case

class TestStrings(unittest.TestCase):

    def test_is_true(self):
        for value in TRUE_VALUES:
            assert_that(is_true(value), is_(True))

    def test_is_false(self):
        for value in FALSE_VALUES:
            assert_that(is_false(value), is_(True))
            
    def test_equals_ignore_case(self):
        assert_that(equals_ignore_case("foo", "Foo"),
                    is_(True))
        assert_that(equals_ignore_case(u'å', u'å'),
                    is_(True))
        assert_that(equals_ignore_case(u'å', u'ß'),
                    is_(False))
        assert_that(equals_ignore_case(u'bar', 'Foo'),
                    is_(False))

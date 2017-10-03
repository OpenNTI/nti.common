#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import unittest

from nti.common.string import TRUE_VALUES
from nti.common.string import FALSE_VALUES

from nti.common.string import is_true
from nti.common.string import is_false


class TestStrings(unittest.TestCase):

    def test_is_true(self):
        for value in TRUE_VALUES:
            assert_that(is_true(value), is_(True))

    def test_is_false(self):
        for value in FALSE_VALUES:
            assert_that(is_false(value), is_(True))

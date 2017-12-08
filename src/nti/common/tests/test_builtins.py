#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that

import unittest

from nti.common.builtins import integer_bit_size
from nti.common.builtins import integer_bit_length


class TestBuiltins(unittest.TestCase):

    def test_integer_bit_length(self):
        assert_that(integer_bit_length(0), is_(0))

        assert_that(integer_bit_length(-10),
                    is_(integer_bit_length(10)))
        
    def test_integer_bit_size(self):
        assert_that(integer_bit_size(0), is_(1))

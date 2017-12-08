#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import has_length
from hamcrest import assert_that

import unittest

from nti.common.random import generate_random_bits
from nti.common.random import generate_random_string
from nti.common.random import generate_random_password
from nti.common.random import generate_random_sequence
from nti.common.random import generate_random_hex_string
from nti.common.random import generate_random_uint_atmost
from nti.common.random import generate_random_uint_between


class TestRandom(unittest.TestCase):

    def test_generate_random_bits(self):
        assert_that(generate_random_bits(15), has_length(2))
        with self.assertRaises(TypeError):
            generate_random_bits(3.5)
        with self.assertRaises(ValueError):
            generate_random_bits(0)

    def test_generate_random_uint_atmost(self):
        with self.assertRaises(TypeError):
            generate_random_uint_atmost(3.5)
        with self.assertRaises(ValueError):
            generate_random_uint_atmost(0)

    def test_generate_random_uint_between(self):
        with self.assertRaises(TypeError):
            generate_random_uint_between(3.5, 6)
        with self.assertRaises(ValueError):
            generate_random_uint_between(3, 3)

        generate_random_uint_between(1, 10000)

    def test_generate_random_sequence(self):
        with self.assertRaises(TypeError):
            generate_random_sequence(3.5, ())
        with self.assertRaises(ValueError):
            generate_random_sequence(0, ())

    def test_generate_random_password(self):
        assert_that(generate_random_password(), has_length(10))

    def test_generate_random_string(self):
        assert_that(generate_random_string(15), has_length(15))

    def test_generate_random_hex_string(self):
        assert_that(generate_random_hex_string(8), has_length(8))
        with self.assertRaises(ValueError):
            generate_random_hex_string(-1)

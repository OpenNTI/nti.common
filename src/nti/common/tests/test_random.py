#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import has_length
from hamcrest import assert_that

import unittest

from nti.common.random import generate_random_bits
from nti.common.random import generate_random_string
from nti.common.random import generate_random_password
from nti.common.random import generate_random_hex_string

class TestRandom(unittest.TestCase):

    def test_generate_random_bits(self):
        assert_that(generate_random_bits(15), has_length(2))

    def test_generate_random_password(self):
        assert_that(generate_random_password(), has_length(10))

    def test_generate_random_string(self):
        assert_that(generate_random_string(15), has_length(15))
    
    def test_generate_random_hex_string(self):
        assert_that(generate_random_hex_string(8), has_length(8))

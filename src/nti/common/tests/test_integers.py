#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

import unittest

from nti.common.integer import bytes_to_uint


class TestIntegers(unittest.TestCase):

    def test_bytes_to_uint(self):
        with self.assertRaises(TypeError):
            bytes_to_uint(u'unicode')

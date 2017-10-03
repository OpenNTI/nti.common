#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

from nti.common.integer import bytes_to_uint


class TestIntegers(unittest.TestCase):

    def test_bytes_to_uint(self):
        with self.assertRaises(TypeError):
            bytes_to_uint(u'unicode')

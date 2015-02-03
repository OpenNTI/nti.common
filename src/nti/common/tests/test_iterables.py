#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that

import unittest
import itertools

from nti.common.iterables import isorted
from nti.common.iterables import IterableWrapper

class TestIterables(unittest.TestCase):

	def test_wrapper(self):
		a = range(1, 6)
		b = range(6, 11)
		w = IterableWrapper(itertools.chain(a, b), 10)
		assert_that(w, has_length(10))
		assert_that(list(w), has_length(10))

		w = IterableWrapper(itertools.chain(a, b), 10)
		assert_that(w[4], is_(5))

		w = IterableWrapper(itertools.chain(a, b), 10)
		assert_that(w[4:6], is_([5, 6]))

	def test_istored(self):
		l =  [2, 1, 5, 3, 7, 9, 4]
		r = list(isorted(l))
		assert_that(r, is_([1, 2, 3, 4, 5, 7, 9]))
		
		comparator = lambda x,y : x > y
		r = list(isorted(l, comparator))
		assert_that(r, is_([9, 7, 5, 4, 3, 2, 1]))

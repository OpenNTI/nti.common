#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import same_instance

import unittest
import itertools

from nti.common.iterables import unique
from nti.common.iterables import flatten
from nti.common.iterables import isorted
from nti.common.iterables import to_list
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
        l = [2, 1, 5, 3, 7, 9, 4]
        r = list(isorted(l))
        assert_that(r, is_([1, 2, 3, 4, 5, 7, 9]))

        def comparator(x, y):
            return x > y
        r = list(isorted(l, comparator))
        assert_that(r, is_([9, 7, 5, 4, 3, 2, 1]))

    def test_unique(self):
        l = [2, 1, 5, 3, 7, 9, 4]
        r = list(unique(l))
        assert_that(r, is_([2, 1, 5, 3, 7, 9, 4]))

        l = [2, 2, 2, 2, 1, 1, 2]
        r = list(unique(l))
        assert_that(r, is_([2, 1]))

    def test_flatten(self):
        l1 = ([2, 1], [3, 4], (5.5,))
        r = list(flatten(l1, tuple))
        assert_that(r, is_([2, 1, 3, 4, (5.5,)]))

    def test_to_list(self):
        l = (5.5,)
        assert_that(to_list(l), is_([5.5]))
        l = (5, 5)
        assert_that(to_list(l), is_([5, 5]))
        l = {5, 4}
        assert_that(sorted(to_list(l)), is_([4, 5]))
        l = 'ichigo'
        assert_that(to_list(l), is_(['ichigo']))
        l = [1, 2, 3]
        assert_that(to_list(l), is_(same_instance(l)))
        l = object()
        assert_that(to_list(l), is_([l]))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

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
from nti.common.iterables import is_nonstr_iterable


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
        
        r = list(unique([[]]))
        assert_that(r, is_([[]]))

    def test_flatten(self):
        l1 = ([2, 1], [3, 4], (5.5,))
        r = list(flatten(l1, tuple))
        assert_that(r, is_([2, 1, 3, 4, (5.5,)]))
        
        l1 = (['ab'], [3, 4])
        r = list(flatten(l1, tuple))
        assert_that(r, is_(['a', 'b', 3, 4]))

    def test_to_list(self):
        assert_that(to_list(None, ()), is_(()))
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

    def test_is_nonstr_iterable(self):
        assert_that(is_nonstr_iterable('d'), is_(False))
        assert_that(is_nonstr_iterable(object()), is_(False))
        
        assert_that(is_nonstr_iterable(set()), is_(True))
        assert_that(is_nonstr_iterable(list()), is_(True))
        assert_that(is_nonstr_iterable(tuple()), is_(True))

        def sample():
            yield 5
            
        assert_that(is_nonstr_iterable(sample()), is_(True))
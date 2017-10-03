#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for working with iterables/sequences.

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from six import binary_type
from six import string_types

from six.moves import filter

from collections import Iterable

from itertools import tee
from itertools import islice

logger = __import__('logging').getLogger(__name__)


class IterableWrapper(object):

    def __init__(self, it, size=0):
        self.it = it
        self.size = size

    def __len__(self):
        return self.size

    def __iter__(self):
        for elt in self.it:
            yield elt

    def __getitem__(self, index):
        if type(index) is slice:
            return list(islice(self.it, index.start, index.stop, index.step))
        else:
            return next(islice(self.it, index, index + 1))


def isorted(iterable, comparator=None):
    """
    generator-based quicksort.

    http://code.activestate.com/recipes/280501-lazy-sorting/
    """
    try:
        iterable = iter(iterable)
        pivot = next(iterable)
    except (TypeError, StopIteration):
        return

    comparator = comparator if comparator else lambda x, y: x < y

    a, b = tee(iterable)
    for x in isorted(filter(lambda x: comparator(x, pivot), a), comparator):
        yield x
    yield pivot
    for x in isorted(filter(lambda x: not comparator(x, pivot), b), comparator):
        yield x


def unique(iterable, seen=None):
    """
    Yields items from the given `iterable` of (hashable) items, once seen an
    item is not yielded again.
    """
    seen_unhashable = []
    seen = set() if seen is None else set(seen)
    for item in iterable:
        try:
            if item not in seen:
                seen.add(item)
                yield item
        except TypeError:
            if item not in seen_unhashable:
                seen_unhashable.append(item)
                yield item


def flatten(iterable, ignore=None):
    """
    Flattens a nested `iterable`.

    :param ignore:
            Types of iterable objects which should be yielded as-is.
    """
    stack = [iter(iterable)]
    while stack:
        try:
            item = next(stack[-1])
            if ignore and isinstance(item, ignore):
                yield item
            elif    (isinstance(item, string_types) or isinstance(item, binary_type)) \
                and len(item) == 1:
                yield item
            else:
                try:
                    stack.append(iter(item))
                except TypeError:
                    yield item
        except StopIteration:
            stack.pop()


def to_list(items=None, default=None):
    if items is None:
        result = default
    elif isinstance(items, string_types):
        result = [items]
    elif isinstance(items, list):
        result = items
    elif isinstance(items, Iterable):
        result = list(items)
    else:
        result = [items]
    return result


import zope.deferredimport
zope.deferredimport.initialize()

zope.deferredimport.deprecatedFrom(
    "Use to pyramid.compat",
    "pyramid.compat",
    "is_nonstr_iter",
)

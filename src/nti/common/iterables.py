#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for working with iterables/sequences.

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from collections import Iterable

from itertools import tee
from itertools import islice
from itertools import ifilter

from nti.common._compat import string_types


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
        pivot = iterable.next()
    except (TypeError, StopIteration):
        return

    comparator = comparator if comparator else lambda x, y: x < y

    a, b = tee(iterable)
    for x in isorted(ifilter(lambda x: comparator(x, pivot), a), comparator):
        yield x
    yield pivot
    for x in isorted(ifilter(lambda x: not comparator(x, pivot), b), comparator):
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


from nti.common import builtins


def flatten(iterable, ignore=None):
    """
    Flattens a nested `iterable`.

    :param ignore:
            Types of iterable objects which should be yielded as-is.
    """
    stack = [iter(iterable)]
    while stack:
        try:
            item = stack[-1].next()
            if ignore and isinstance(item, ignore):
                yield item
            elif builtins.is_bytes_or_unicode(item) and len(item) == 1:
                yield item
            else:
                try:
                    stack.append(iter(item))
                except TypeError:
                    yield item
        except StopIteration:
            stack.pop()


import itertools

try:
    from itertools import izip
except ImportError:
    izip = zip


def izip_longest(*iterables, **kwargs):
    """
    Make an iterator that aggregates elements from each of the iterables. If
    the iterables are of uneven length, missing values are filled-in with
    `fillvalue`. Iteration continues until the longest iterable is exhausted.

    If one of the iterables is potentially infinite, then the
    :func:`izip_longest` function should be wrapped with something that limits
    the number of calls (for example :func:`itertools.islice` or
    :func:`itertools.takewhile`.) If not specified, `fillvalue` defaults to
    ``None``.

    .. note:: Software and documentation for this function are taken from
                      CPython, :ref:`license details <psf-license>`.
    """
    fillvalue = kwargs.get("fillvalue")

    def sentinel(counter=([fillvalue] * (len(iterables) - 1)).pop):
        yield counter()

    fillers = itertools.repeat(fillvalue)
    iters = [itertools.chain(it, sentinel(), fillers) for it in iterables]
    try:
        for tup in izip(*iters):
            yield tup
    except IndexError:
        pass


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

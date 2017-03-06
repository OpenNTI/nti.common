#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for working with iterables/sequences.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from collections import Iterable

from itertools import tee
from itertools import islice
from itertools import ifilter

from nti.common._compat import PY3
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


def product(*iterables, **kwargs):
    """
    Cartesian product of input iterables.

    Equivalent to nested for-loops in a generator expression. For example,
    ``product(A, B)`` returns the same as ``((x, y) for x in A for y in B)``.

    The nested loops cycle like an odometer with the rightmost element
    advancing on every iteration. The pattern creates a lexicographic ordering
    so that if the input's iterables are sorted, the product tuples are emitted
    in sorted order.

    To compute the product of an iterable with itself, specify the number of
    repetitions with the optional `repeat` keyword argument. For example,
    ``product(A, repeat=4)`` means the same as ``product(A, A, A, A)``.

    .. note:: Software and documentation for this function are taken from
                      CPython, :ref:`license details <psf-license>`.
    """
    pools = map(tuple, iterables) * kwargs.get("repeat", 1)
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def permutations(iterable, r=None):
    """
    Return successive `r` length permutations of elements in the `iterable`.

    If `r` is not specified or is ``None``, then `r` defaults to the length of
    the `iterable` and all possible full-length permutations are generated.

    Permutations are emitted in lexicographic sort order. So, if the input
    `iterable` is sorted, the permutation tuples will be produced in sorted
    order.

    Elements are treated as unique based on their position, not on their
    value. So if the input elements are unique, there will be no repeating
    value in each permutation.

    The number of items returned is ``n! / (n - r)!`` when ``0 <= r <= n`` or
    zero when `r > n`.

    .. note:: Software and documentation for this function are taken from
                      CPython, :ref:`license details <psf-license>`.
    """
    pool = tuple(iterable)
    pool_length = len(pool)
    r = pool_length if r is None else r
    for indices in product(xrange(pool_length), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)

if PY3:  # pragma: no cover
    def is_nonstr_iter(v):
        if isinstance(v, str):
            return False
        return hasattr(v, '__iter__')
else:
    def is_nonstr_iter(v):
        return hasattr(v, '__iter__')


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

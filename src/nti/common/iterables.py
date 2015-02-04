#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for working with iterables/sequences.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from itertools import ifilter, tee, islice

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

	comparator = comparator if comparator else lambda x,y: x < y
		
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

from . import builtins

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

from ._compat import PY3

if PY3: # pragma: no cover
	def is_nonstr_iter(v):
		if isinstance(v, str):
			return False
		return hasattr(v, '__iter__')
else:
	def is_nonstr_iter(v):
		return hasattr(v, '__iter__')

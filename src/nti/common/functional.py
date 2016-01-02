#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import itertools
from functools import reduce

def compose(function, *functions):
	"""
	Composes a sequence of functions such that::

		compose(g, f, s) -> g(f(s()))

	:param functions:
		An iterable of functions.
	:returns:
		A composition function.
	"""

	def _composition(a_func, b_func):
		def _wrap(*args, **kwargs):
			return a_func(b_func(*args, **kwargs))
		return _wrap
	return reduce(_composition, functions, function)

def complement(predicate):
	"""
	Generates a complementary predicate function for the given predicate
	function.

	:param predicate:
		Predicate function.
	:returns:
		Complementary predicate function.
	"""

	def _negate(*args, **kwargs):
		return not predicate(*args, **kwargs)
	return _negate

def partition(predicate, iterable):
	"""
	Partitions an iterable into two iterables where for the elements of
	one iterable the predicate is true and for those of the other it is false.

	:param predicate:
		Function of the format::

			f(x) -> bool
	:param iterable:
		Iterable sequence.
	:returns:
		Tuple (selected, rejected)
	"""

	def _partitioner(memo, item):
		part = memo[0] if predicate(item) else memo[1]
		part.append(item)
		return memo
	return tuple(reduce(_partitioner, iterable, [[], []]))

def _get_iter_next(iterator):
	"""
	Gets the next item in the iterator.
	"""
	attr = getattr(iterator, "next", None)
	if not attr:
		attr = getattr(iterator, "__next__")
	return attr

def round_robin(*iterables):
	"""
	Returns items from the iterables in a round-robin fashion.

	Taken from the Python documentation. Under the PSF license.
	Recipe credited to George Sakkis

	Example::

		round_robin("ABC", "D", "EF") --> A D E B F C"

	:param iterables:
		Variable number of inputs for iterable sequences.
	:yields:
		Items from the iterable sequences in a round-robin fashion.
	"""
	pending = len(iterables)
	nexts = itertools.cycle(_get_iter_next(iter(it)) for it in iterables)
	while pending:
		try:
			for next_ in nexts:
				yield next_()
		except StopIteration:
			pending -= 1
			nexts = itertools.cycle(itertools.islice(nexts, pending))

def ncycles(iterable, times):
	"""
	Yields the sequence elements n times.

	Taken from the Python documentation. Under the PSF license.

	:param iterable:
		Iterable sequence.
	:param times:
		The number of times to yield the sequence.
	:yields:
		Iterator.
	"""
	chain = itertools.chain
	return chain.from_iterable(itertools.repeat(tuple(iterable), times))

def identity(arg):
	"""
	Identity function. Produces what it consumes.

	:param arg:
		Argument
	:returns:
		Argument.
	"""
	return arg

def setattribute(obj, name, value):
	"""
	Set a named attribute on an object;
	"""
	setattr(obj, name, value)

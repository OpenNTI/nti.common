#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


def choose(n, k, *unused_args):
    """
    A fast way to calculate binomial coefficients.
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0


def combinations(N, k, *unused_args):
    """
    The number of combinations of N things taken k at a time
    """
    if (k > N) or (N < 0) or (k < 0):
        return 0L
    N, k = map(long, (N, k))
    top = N
    val = 1L
    while (top > (N - k)):
        val *= top
        top -= 1
    n = 1L
    while (n < k + 1L):
        val /= n
        n += 1
    return val

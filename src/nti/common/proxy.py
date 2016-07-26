#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

try:
	from nti.externalization.proxy import removeAllProxies
except ImportError:
	from nti.common._proxy import removeAllProxies

removeAllProxies = removeAllProxies # pylint

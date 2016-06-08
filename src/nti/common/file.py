#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re

_nameFinder = re.compile(r'(.*[\\/:])?(.+)')

def name_finder(filename):
	match = _nameFinder.match(filename) if filename else None
	result = match.group(2) if match else None
	return result
nameFinder = name_finder

def safe_filename(s):
	return re.sub(r'[/<>:"\\|?*]+', '_', s) if s else s

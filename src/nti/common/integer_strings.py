#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

try:
	from nti.externalization.integer_strings import from_external_string
except ImportError:
	from nti.common._external import from_external_string

from_external_string = from_external_string # pylint

try:
	from nti.externalization.integer_strings import to_external_string
except ImportError:
	from nti.common._external import to_external_string

to_external_string = to_external_string # pylint

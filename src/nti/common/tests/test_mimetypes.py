#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import unittest

from nti.common.mimetypes import guess_type

class TestMimeTypes(unittest.TestCase):
	
	def test_guess_type(self):
		t = guess_type('foo.xml')
		assert_that(t[0], is_('application/xml'))
		t = guess_type('foo.mml')
		assert_that(t[0], is_('text/mathml'))
		assert_that(guess_type(None), is_((None, None)))


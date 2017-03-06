#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_entry
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

import sys
import unittest

from nti.common.deprecated import moved


class TestDeprecated(unittest.TestCase):

    def test_moved(self):
        old = moved('nti.common.oldsets', 'nti.common.sets')
        assert_that(old, is_not(none()))
        assert_that(old, has_property('discard', is_not(none())))
        assert_that(sys.modules, has_entry('nti.common.oldsets', is_(old)))
        # check import
        __import__('nti.common.oldsets')

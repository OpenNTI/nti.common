#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property

import unittest

import nameparser

from nti.common.nameparser import constants
from nti.common.nameparser import all_suffixes
from nti.common.nameparser import get_suffixes

class TestNameParser(unittest.TestCase):

    def test_name_parser(self):
        assert_that(all_suffixes(), has_length(103))
        assert_that(get_suffixes(), has_length(103))

    def test_human_name(self):
        realname = "Ichigo Kurosaki, cfa"
        name = nameparser.HumanName(realname,
                                    constants=constants(extra_suffixes=('cfa',)))
        assert_that(name, has_property('suffix', is_('cfa')))

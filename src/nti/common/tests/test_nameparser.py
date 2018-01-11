#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property

import unittest

from nti.common.nameparser import human_name
from nti.common.nameparser import all_prefixes
from nti.common.nameparser import all_suffixes
from nti.common.nameparser import get_suffixes

class TestNameParser(unittest.TestCase):
        
    def test_name_parser(self):
        assert_that(all_prefixes(), has_length(28))
        assert_that(all_suffixes(), has_length(105))
        assert_that(get_suffixes(), has_length(105))

    def test_human_name(self):
        realname = "Ichigo Kurosaki, cfa"
        name = human_name(realname, extra_suffixes=('cfa',))
        assert_that(name, has_property('suffix', is_('cfa')))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import has_length
from hamcrest import assert_that

import unittest

from nti.common.hash import md5_digest
from nti.common.hash import sha1_digest
from nti.common.hash import sha1_hex_digest
from nti.common.hash import sha1_base64_digest


class TestHash(unittest.TestCase):

    strings = (b'ichigo', b'aizen')

    def test_md5_digest(self):
        assert_that(md5_digest(*self.strings), has_length(16))
        
    def test_sha1_digest(self):
        assert_that(sha1_digest(*self.strings), has_length(20))
    
    def test_sha1_hex_digest(self):
        assert_that(sha1_hex_digest(*self.strings), has_length(40))
    
    def test_sha1_base64_digest(self):
        assert_that(sha1_base64_digest(*self.strings), has_length(28))

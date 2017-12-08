#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that

import unittest

from nti.common.hash import md5_digest
from nti.common.hash import sha1_digest
from nti.common.hash import md5_hex_digest
from nti.common.hash import sha1_hex_digest
from nti.common.hash import hmac_sha1_digest
from nti.common.hash import md5_base64_digest
from nti.common.hash import sha1_base64_digest
from nti.common.hash import hmac_sha1_base64_digest


class TestHash(unittest.TestCase):

    strings = ('ichigo', 'aizen')

    def test_md5_digest(self):
        assert_that(md5_digest(*self.strings), has_length(16))
        
    def test_md5_hex_digest(self):
        assert_that(md5_hex_digest(*self.strings), has_length(32))

    def test_md5_base64_digest(self):
        assert_that(md5_base64_digest(*self.strings), 
                    is_(b'TuRG3A/YhLz8XwN0fYRKEw=='))

    def test_sha1_digest(self):
        assert_that(sha1_digest(*self.strings), has_length(20))
    
    def test_sha1_hex_digest(self):
        assert_that(sha1_hex_digest(*self.strings), has_length(40))
    
    def test_sha1_base64_digest(self):
        assert_that(sha1_base64_digest(*self.strings), has_length(28))

    def test_hmac_sha1_digest(self):
        assert_that(hmac_sha1_digest(*self.strings), has_length(20))
        
    def test_hmac_sha1_base64_digest(self):
        assert_that(hmac_sha1_base64_digest(*self.strings),
                    is_(b'R0H/Ra45J3wmyLOQ74ss1O2E9kQ='))
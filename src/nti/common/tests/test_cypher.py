#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that

import unittest

from nti.common.cypher import is_base64
from nti.common.cypher import get_plaintext
from nti.common.cypher import make_ciphertext


class TestCypher(unittest.TestCase):

    def test_symmetrical(self):
        text = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
        ciphertext = make_ciphertext(text)
        assert_that(ciphertext, is_not(text))
        plaintext = get_plaintext(ciphertext)
        assert_that(plaintext, is_(text))

    def test_isb64(self):
        text = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
        assert_that(is_base64(text), is_(False))
        assert_that(is_base64('TjN4dFRoMHVnaHQhIUM='), is_(True))
        assert_that(is_base64(u'いちご='), is_(False))

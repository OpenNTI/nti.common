#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import raises
from hamcrest import calling
from hamcrest import assert_that

import unittest

from nti.common import phonenumbers


class TestPhoneNumbers(unittest.TestCase):

    def test_limit(self):
        assert_that(calling(phonenumbers._limit).with_args(2,1),
                    raises(Exception))

    def test_is_viable_phone_number(self):
        assert_that(phonenumbers.is_viable_phone_number('1'),
                    is_(False))

        assert_that(phonenumbers.is_viable_phone_number('(14)a'),
                    is_(False))

        assert_that(phonenumbers.is_viable_phone_number('14052497426'),
                    is_(True))

        assert_that(phonenumbers.is_viable_phone_number('1-405-249-7426'),
                    is_(True))

        assert_that(phonenumbers.is_viable_phone_number('+1-504-249-7426'),
                    is_(True))

        assert_that(phonenumbers.is_viable_phone_number('+1 (504) 249-7426'),
                    is_(True))

        assert_that(phonenumbers.is_viable_phone_number('011 (57) 315 403-5341'),
                    is_(True))

        assert_that(phonenumbers.is_viable_phone_number('+62 812 57076743'),
                    is_(True))

        assert_that(phonenumbers.is_viable_phone_number('ichigo kurosaki'),
                    is_(False))

        assert_that(phonenumbers.is_viable_phone_number('ichigo 4057464'),
                    is_(False))

        assert_that(phonenumbers.is_viable_phone_number('1-800-flowers'),
                    is_(True))

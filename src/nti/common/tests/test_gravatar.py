#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that

import unittest

from nti.common import create_gravatar_url


class TestGravatar(unittest.TestCase):

    def test_create_gravatar_url(self):

        assert_that(create_gravatar_url('jason.madden@nextthought.com'),
                    is_('http://www.gravatar.com/avatar/5738739998b683ac8fe23a61c32bb5a0?s=128&d=mm'))

        assert_that(create_gravatar_url('jason.madden@nextthought.com', secure=True),
                    is_('https://secure.gravatar.com/avatar/5738739998b683ac8fe23a61c32bb5a0?s=128&d=mm'))

        assert_that(create_gravatar_url('jason.madden@nextthought.com', defaultGravatarType='wavatar'),
                    is_('http://www.gravatar.com/avatar/5738739998b683ac8fe23a61c32bb5a0?s=128&d=wavatar'))

        assert_that(create_gravatar_url('jason.madden@nextthought.com', size=512),
                    is_('http://www.gravatar.com/avatar/5738739998b683ac8fe23a61c32bb5a0?s=512&d=mm'))

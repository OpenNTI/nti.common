#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from nti.testing.layers import GCLayerMixin
from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin

import zope.testing.cleanup


class NonDevmodeSharedConfiguringTestLayer(ZopeComponentLayer,
                                           GCLayerMixin,
                                           ConfiguringLayerMixin):

    features = ()
    set_up_packages = ()

    @classmethod
    def setUp(cls):
        cls.setUpPackages()

    @classmethod
    def tearDown(cls):
        cls.tearDownPackages()
        zope.testing.cleanup.cleanUp()

    @classmethod
    def testSetUp(cls, test=None):  # pylint: disable=arguments-differ
        pass

    @classmethod
    def testTearDown(cls):
        pass

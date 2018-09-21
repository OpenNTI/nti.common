#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods
from nti.testing.layers import ConfiguringLayerMixin
from nti.testing.layers import GCLayerMixin
from nti.testing.layers import ZopeComponentLayer

import zope.testing.cleanup

from nti.dataserver.tests import DSInjectorMixin


class NonDevmodeSharedConfiguringTestLayer(ZopeComponentLayer,
                                           GCLayerMixin,
                                           ConfiguringLayerMixin,
                                           DSInjectorMixin):

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
    def testSetUp(cls, test=None):
        cls.setUpTestDS(test)

    @classmethod
    def testTearDown(cls):
        pass

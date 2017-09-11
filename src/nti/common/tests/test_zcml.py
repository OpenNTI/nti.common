#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_property

from nti.testing.matchers import verifiably_provides

from zope import component

from nti.common.interfaces import IAWSKey

import nti.testing.base

KEY_ZCML_STRING = u"""
<configure xmlns="http://namespaces.zope.org/zope"
	xmlns:zcml="http://namespaces.zope.org/zcml"
	xmlns:aws="http://nextthought.com/ntp/aws"
	i18n_domain='nti.dataserver'>

	<include package="zope.component" />
	<include package="z3c.baseregistry" file="meta.zcml" />
	
	<include package="." file="meta.zcml" />

	<aws:registerAWSKey
		purpose="S3"
		grant="private-read-write"
		bucket_name="nti-dataserver-dev"
		access_key="AKIAIYVGOCPVO6AQRILQ"
		secret_key="aws_s3_secret_access_key" />
</configure>
"""


class TestZcml(nti.testing.base.ConfiguringTestBase):

	def test_aws_registration(self):
		self.configure_string(KEY_ZCML_STRING)
		awskey = component.queryUtility(IAWSKey, "S3")
		assert_that(awskey, is_not(none()))
		assert_that(awskey, verifiably_provides(IAWSKey))
		assert_that(awskey, 
					has_property('Purpose', "S3"))
		assert_that(awskey, 
					has_property('Grant', "private-read-write"))
		assert_that(awskey, 
					has_property('Bucket', "nti-dataserver-dev"))
		assert_that(awskey, 
					has_property('PublicAccessKey', "AKIAIYVGOCPVO6AQRILQ"))
		assert_that(awskey, 
					has_property('SecretAccessKey', "aws_s3_secret_access_key"))
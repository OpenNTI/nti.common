#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_property

from nti.testing.matchers import verifiably_provides

from zope import component

from nti.common.interfaces import ILDAP
from nti.common.interfaces import IAWSKey
from nti.common.interfaces import IOAuthKeys

import nti.testing.base

HEAD_ZCML_STRING = u"""
<configure xmlns="http://namespaces.zope.org/zope"
	xmlns:zcml="http://namespaces.zope.org/zcml"
	xmlns:aws="http://nextthought.com/ntp/aws"
	xmlns:ldap="http://nextthought.com/ntp/ldap"
	xmlns:oauth="http://nextthought.com/ntp/oauth"
	i18n_domain='nti.dataserver'>

	<include package="zope.component" />
	<include package="zope.annotation" />
	
	<include package="." file="meta.zcml" />

"""

AWS_ZCML_STRING = HEAD_ZCML_STRING + u"""
	<aws:registerAWSKey
		purpose="S3"
		grant="private-read-write"
		bucket_name="nti-dataserver-dev"
		access_key="AKIAIYVGOCPVO6AQRILQ"
		secret_key="aws_s3_secret_access_key" />
</configure>
"""

LDAP_ZCML_STRING = HEAD_ZCML_STRING + u"""
	<ldap:registerLDAP
		id="nti-ldap"
		url="ldaps://ldaps.nextthought.com:636"
		username="jason.madden@nextthougt.com"
		password="aWNoaWdv\n"
		encoding="base64"
		baseDN="OU=Accounts" />
</configure>
"""

OAUTHKEYS_ZCML_STRING = HEAD_ZCML_STRING + u"""
	<oauth:registerOAuthKeys
		apiKey="abcd12345"
		secretKey="efgh56789" />
</configure>
"""


class TestZcml(nti.testing.base.ConfiguringTestBase):

    def test_aws_registration(self):
        self.configure_string(AWS_ZCML_STRING)
        awskey = component.queryUtility(IAWSKey, "S3")
        assert_that(awskey, is_not(none()))
        assert_that(awskey, verifiably_provides(IAWSKey))
        assert_that(awskey,
                    has_property('Purpose', "S3"))
        assert_that(awskey,
                    has_property('Grant', "private-read-write"))
        assert_that(awskey,
                    has_property('BucketName', "nti-dataserver-dev"))
        assert_that(awskey,
                    has_property('PublicAccessKey', "AKIAIYVGOCPVO6AQRILQ"))
        assert_that(awskey,
                    has_property('SecretAccessKey', "aws_s3_secret_access_key"))

    def test_ldap_registration(self):
        self.configure_string(LDAP_ZCML_STRING)
        ldap = component.queryUtility(ILDAP, name="nti-ldap")
        assert_that(ldap, is_not(none()))
        assert_that(ldap, verifiably_provides(ILDAP))
        assert_that(ldap, 
					has_property('URL', "ldaps://ldaps.nextthought.com:636"))
        assert_that(ldap, 
					has_property('Username', "jason.madden@nextthougt.com"))
        assert_that(ldap, has_property('Password', "ichigo"))
        assert_that(ldap, has_property('BaseDN', "OU=Accounts"))

    def test_oauth_registration(self):
        self.configure_string(OAUTHKEYS_ZCML_STRING)
        keys = component.getUtility(IOAuthKeys)
        assert_that(keys, verifiably_provides(IOAuthKeys))
        assert_that(keys, has_property('APIKey', "abcd12345"))
        assert_that(keys, has_property('SecretKey', "efgh56789"))

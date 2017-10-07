#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from nti.common.interfaces import ILDAP
from nti.common.interfaces import IAWSKey
from nti.common.interfaces import IOAuthKeys

from nti.property.property import alias

from nti.schema.eqhash import EqHash

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured

logger = __import__('logging').getLogger(__name__)


@EqHash('PublicAccessKey', 'Purpose')
@interface.implementer(IAWSKey)
class AWSKey(SchemaConfigured):
    createDirectFieldProperties(IAWSKey)

    grant = alias('Grant')
    purpose = alias('Purpose')
    bucket_name = alias('BucketName')
    access_key = alias('PublicAccessKey')
    secret_key = alias('SecretAccessKey')


@EqHash('ID')
@interface.implementer(ILDAP)
class LDAP(SchemaConfigured):
    createDirectFieldProperties(ILDAP)

    name = id = alias('ID')
    password = alias('Password')

    def __str__(self):
        return self.URL


@EqHash('APIKey', 'SecretKey')
@interface.implementer(IOAuthKeys)
class OAuthKeys(SchemaConfigured):
    createDirectFieldProperties(IOAuthKeys)

    id = apiKey = alias('APIKey')
    secretKey = alias('SecretKey')

    def __str__(self):
        return self.APIKey

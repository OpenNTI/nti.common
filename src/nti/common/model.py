#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines an ldap registration object

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.common._compat import text_

from nti.common.cypher import is_base64
from nti.common.cypher import get_plaintext

from nti.common.interfaces import ILDAP
from nti.common.interfaces import IAWSKey
from nti.common.interfaces import IOAuthKeys

from nti.property.property import alias

from nti.schema.eqhash import EqHash

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured


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

    def __setattr__(self, name, value):
        if name in ("Password", "password"):
            try:
                if is_base64(value):
                    value = text_(get_plaintext(value))
            except Exception:
                pass
        return SchemaConfigured.__setattr__(self, name, value)


@EqHash('APIKey', 'SecretKey')
@interface.implementer(IOAuthKeys)
class OAuthKeys(SchemaConfigured):
    createDirectFieldProperties(IOAuthKeys)

    id = apiKey = alias('APIKey')
    secretKey = alias('SecretKey')

    def __str__(self):
        return self.APIKey

    def __setattr__(self, name, value):
        if name in ("apiKey", "APIKey", "secretKey", "SecretKey", 'id'):
            try:
                if is_base64(value):
                    value = text_(get_plaintext(value))
            except Exception:
                pass
        return SchemaConfigured.__setattr__(self, name, value)

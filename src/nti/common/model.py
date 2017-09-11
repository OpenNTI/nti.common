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

from nti.common.interfaces import IAWSKey

from nti.property.property import alias

from nti.schema.eqhash import EqHash

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured


@EqHash('PublicAccessKey', 'Purpose')
@interface.implementer(IAWSKey)
class AWSKey(SchemaConfigured):
    createDirectFieldProperties(IAWSKey)

    purpose = alias('Purpose')
    bucket_name = alias('Bucket')
    access_key = alias('PublicAccessKey')
    secret_key = alias('SecretAccessKey')

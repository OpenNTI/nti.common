#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
Directives to be used in ZCML: registering static keys.

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import functools

from zope import interface

from zope.component.zcml import utility

from zope.configuration import fields

from nti.common._compat import text_

from nti.common.interfaces import IAWSKey 

from nti.common.model import AWSKey 


class IRegisterAWSKey(interface.Interface):
    """
    The arguments needed for registering an AWS key
    """
    name = fields.TextLine(title=u"key name", required=False)
    bucket_name = fields.TextLine(title=u"Bucket name", required=False)
    purpose = fields.TextLine(title=u"Key purpose", required=True)
    access_key = fields.TextLine(title=u"Access key", required=True)
    secret_key = fields.TextLine(title=u"Secret key", required=True)


def registerAWSKey(_context, access_key, secret_key, purpose, 
                   bucket_name=None, name=''):
    """
    Register an aws key
    """
    name = name or ''
    bucket_name = text_(bucket_name) if bucket_name else bucket_name
    factory = functools.partial(AWSKey, 
                                Bucket=bucket_name,
                                Purpose=text_(purpose),
                                PublicAccessKey=text_(access_key), 
                                SecretAccessKey=text_(secret_key))
    utility(_context, provides=IAWSKey, factory=factory, name=name)

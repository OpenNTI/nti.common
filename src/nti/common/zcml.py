#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
Directives to be used in ZCML: registering static keys.

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import base64
import urllib
import functools

from zope import schema
from zope import interface

from zope.component.zcml import utility

from zope.configuration import fields

from nti.common._compat import text_

from nti.common.interfaces import ILDAP
from nti.common.interfaces import IAWSKey
from nti.common.interfaces import IOAuthKeys

from nti.common.model import LDAP
from nti.common.model import AWSKey
from nti.common.model import OAuthKeys

BASE_64 = 'base64'
URL_QUOTE = 'urlquote'
PASSWORD_ENCODING = (URL_QUOTE, BASE_64)


class IRegisterAWSKey(interface.Interface):
    """
    The arguments needed for registering an AWS key
    """
    grant = fields.TextLine(title=u"rant type", required=False)
    bucket_name = fields.TextLine(title=u"Bucket name", required=False)
    purpose = fields.TextLine(title=u"Key purpose", required=True)
    access_key = fields.TextLine(title=u"Access key", required=True)
    secret_key = fields.TextLine(title=u"Secret key", required=True)


def registerAWSKey(_context, access_key, secret_key, purpose,
                   bucket_name=None, grant=None):
    """
    Register an aws key
    """
    grant = text_(grant or 'public-read-write')
    bucket_name = text_(bucket_name) if bucket_name else bucket_name
    factory = functools.partial(AWSKey,
                                Grant=grant,
                                BucketName=bucket_name,
                                Purpose=text_(purpose),
                                PublicAccessKey=text_(access_key),
                                SecretAccessKey=text_(secret_key))
    utility(_context, provides=IAWSKey, factory=factory, name=purpose)


class IRegisterLDAP(interface.Interface):
    """
    The arguments needed for registering an ldap
    """
    id = fields.TextLine(title=u"ldap identifier", required=False)
    url = fields.TextLine(title=u"ldap url", required=True)
    username = fields.TextLine(title=u"Bind username", required=True)
    password = schema.Password(title=u"Bind password", required=True)
    baseDN = fields.TextLine(title=u"Base DN", required=False)
    encoding = fields.TextLine(title=u"Password encoding", required=False)
    backupURL = fields.TextLine(title=u"ldap backup url", required=False)


def registerLDAP(_context, url, username, password, baseDN=None,
                 encoding=None, backupURL=None, **kwargs):
    """
    Register an ldap
    """
    encoding = encoding or ''
    if encoding.lower() == URL_QUOTE:
        password = urllib.unquote(password)
    elif encoding.lower() == BASE_64:
        password = base64.decodestring(password)

    name = kwargs.get('name') or kwargs.get('id') or ''
    factory = functools.partial(LDAP,
                                ID=text_(name),
                                URL=text_(url),
                                Password=password,
                                Username=text_(username),
                                BaseDN=text_(baseDN),
                                BackupURL=text_(backupURL))
    utility(_context, provides=ILDAP, factory=factory, name=name)


class IRegisterOAuthKeys(interface.Interface):
    """
    The arguments needed for registering oauth keys
    """
    id = fields.TextLine(title=u"ouath identifier", required=False)
    apiKey = fields.TextLine(title=u"API key", required=True)
    secretKey = fields.TextLine(title=u"secrent key", required=True)


def registerOAuthKeys(_context, apiKey, secretKey, **kwargs):
    name = kwargs.get('name') or kwargs.get('id') or ''
    factory = functools.partial(OAuthKeys,
                                APIKey=text_(apiKey),
                                SecretKey=secretKey)
    utility(_context, provides=IOAuthKeys, factory=factory, name=name)

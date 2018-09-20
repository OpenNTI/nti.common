#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class
from zope.configuration.config import GroupingContextDecorator
from zope.configuration.interfaces import IConfigurationContext

try:
    from base64 import decodebytes
except ImportError:  # pragma: no cover
    from base64 import decodestring as decodebytes

import functools

from zope import schema
from zope import interface

from zope.component.zcml import utility

from zope.configuration import fields

from nti.common._compat import text_
from nti.common._compat import bytes_

from nti.common.interfaces import ILDAP
from nti.common.interfaces import IAWSKey
from nti.common.interfaces import IOAuthKeys

from nti.common.model import LDAP
from nti.common.model import AWSKey
from nti.common.model import OAuthKeys
from nti.common.cypher import get_plaintext

BASE_64 = 'base64'
PASSWORD_ENCODING = (BASE_64,)

logger = __import__('logging').getLogger(__name__)


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
    if encoding.lower() == BASE_64:
        password = decodebytes(bytes_(password))

    name = kwargs.get('name') or kwargs.get('id') or ''
    factory = functools.partial(LDAP,
                                ID=text_(name),
                                URL=text_(url),
                                Password=text_(password),
                                Username=text_(username),
                                BaseDN=text_(baseDN),
                                BackupURL=text_(backupURL))
    utility(_context, provides=ILDAP, factory=factory, name=name)


class IRegisterOAuthKeys(interface.Interface):
    """
    The arguments needed for registering oauth keys
    """
    id = fields.TextLine(title=u"OAuth identifier", required=False)
    apiKey = fields.TextLine(title=u"API key", required=True)
    secretKey = fields.TextLine(title=u"Secret key", required=True)


def decode(key):
    try:
        return get_plaintext(key)
    except Exception:  # pylint: disable=broad-except
        return key


def registerOAuthKeys(_context, apiKey, secretKey, **kwargs):
    name = kwargs.get('name') or kwargs.get('id') or ''
    factory = functools.partial(OAuthKeys,
                                APIKey=text_(apiKey),
                                SecretKey=text_(decode(secretKey)))
    utility(_context, provides=IOAuthKeys, factory=factory, name=name)


class IWithDebugger(interface.Interface):
    """
    A ZCML directive that starts a debugging session
    before the handler is called for a simple zcml directive
    """


@interface.implementer(IConfigurationContext, IWithDebugger)
class WithDebugger(GroupingContextDecorator):

    def __getattr__(self, item, **kw):
        v = super(WithDebugger, self).__getattr__(item, **kw)
        # We only want to do this when we are
        # getting the directive factory from the registry
        if item =='factory':
            # This is just reading into the parent configuration machine
            def patch_configuration_machine(*args, **kwargs):
                result = v(*args, **kwargs)
                # Here the stack item gets created.
                # We can now access the handler function
                # so we patch in our debugger
                def patch_stack(*args, **kwargs):
                    stack = result(*args, **kwargs)
                    default_handler = stack.handler
                    def debug(*args, **kwargs):
                        # The handler for this registration is about to be called
                        from IPython.terminal.debugger import set_trace;set_trace()
                        return default_handler(*args, **kwargs)
                    stack.handler = debug
                    return stack
                return patch_stack
            return patch_configuration_machine
        return v

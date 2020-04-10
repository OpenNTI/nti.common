#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class
try:
    from base64 import decodebytes
except ImportError:  # pragma: no cover
    from base64 import decodestring as decodebytes

import functools

import pdb

from zope import interface

from zope.component.zcml import utility

from zope.configuration.config import GroupingContextDecorator

from zope.configuration.interfaces import IConfigurationContext

from zope.schema import URI
from zope.schema import Password
from zope.schema import TextLine

from nti.common._compat import text_
from nti.common._compat import bytes_

from nti.common.interfaces import ILDAP
from nti.common.interfaces import IAWSKey
from nti.common.interfaces import IOAuthKeys
from nti.common.interfaces import IOAuthService
from nti.common.interfaces import IContentSigner


from nti.common.model import LDAP
from nti.common.model import AWSKey
from nti.common.model import OAuthKeys
from nti.common.model import ContentSigner
from nti.common.model import ProxyOAuthService
from nti.common.cypher import get_plaintext

BASE_64 = 'base64'
PASSWORD_ENCODING = (BASE_64,)

logger = __import__('logging').getLogger(__name__)


class IRegisterAWSKey(interface.Interface):
    """
    The arguments needed for registering an AWS key
    """
    grant = TextLine(title=u"rant type", required=False)
    bucket_name = TextLine(title=u"Bucket name", required=False)
    purpose = TextLine(title=u"Key purpose", required=True)
    access_key = TextLine(title=u"Access key", required=True)
    secret_key = TextLine(title=u"Secret key", required=True)


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
    id = TextLine(title=u"ldap identifier", required=False)
    url = TextLine(title=u"ldap url", required=True)
    username = TextLine(title=u"Bind username", required=True)
    password = Password(title=u"Bind password", required=True)
    baseDN = TextLine(title=u"Base DN", required=False)
    encoding = TextLine(title=u"Password encoding", required=False)
    backupURL = TextLine(title=u"ldap backup url", required=False)


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
    id = TextLine(title=u"OAuth identifier", required=False)
    apiKey = TextLine(title=u"API key", required=True)
    secretKey = TextLine(title=u"Secret key", required=True)


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


def patch_in_debugger(v, item):
    # We only want to do this when we are
    # getting the directive factory from the registry
    if item == 'factory':
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
                    pdb.set_trace()
                    return default_handler(*args, **kwargs)

                stack.handler = debug
                return stack
            return patch_stack
        return patch_configuration_machine
    return v


@interface.implementer(IConfigurationContext, IWithDebugger)
class WithDebugger(GroupingContextDecorator):

    def __getattr__(self, name):  # pylint: disable=signature-differs
        result = super(WithDebugger, self).__getattr__(name)
        if self.context.hasFeature("devmode"):
            result = patch_in_debugger(result, name)
        else:
            logger.warning(u'A ZCML debugger has been left in %s', self.info)
        return result


class IRegisterOAuthService(interface.Interface):
    """
    The arguments needed for registering an OAuth service
    """
    id = TextLine(title=u"Service identifier", required=False)
    authorization_url = URI(title=u"Authorization Endpoint",
                            description=u"URL for the authorization request")


def registerOAuthService(_context, authorization_url, **kwargs):
    name = kwargs.get('id') or ''
    factory = functools.partial(ProxyOAuthService,
                                authorization_url=text_(authorization_url))
    utility(_context, provides=IOAuthService, factory=factory, name=name)


class IRegisterSigner(interface.Interface):
    """
    The arguments needed for registering the signer.
    """
    id = TextLine(title=u"Signer identifier", required=False)
    secret = TextLine(title=u"Shared secret", required=True)
    salt = TextLine(title=u"Namespace used when creating the hash", required=False)


def registerContentSigner(_context, id=None, secret=None, salt=None):
    """
    Register the signer.
    """
    name = id or ''
    factory = functools.partial(ContentSigner,
                                secret=secret,
                                salt=salt)
    utility(_context, provides=IContentSigner, factory=factory, name=name)

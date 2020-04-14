#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import hashlib
import os

from itsdangerous import URLSafeSerializer

from six.moves import urllib_parse

from zope import component
from zope import interface

from nti.common.cypher import get_plaintext

from nti.common.interfaces import ILDAP
from nti.common.interfaces import IAWSKey
from nti.common.interfaces import IOAuthKeys
from nti.common.interfaces import IOAuthService
from nti.common.interfaces import IContentSigner

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
        return self.URL  # pylint: disable=no-member


@EqHash('APIKey', 'SecretKey')
@interface.implementer(IOAuthKeys)
class OAuthKeys(SchemaConfigured):
    createDirectFieldProperties(IOAuthKeys)

    ClientId = id = apiKey = alias('APIKey')
    ClientSecret = secretKey = alias('SecretKey')

    def __str__(self):
        return self.APIKey  # pylint: disable=no-member


@interface.implementer(IContentSigner)
class ContentSigner(object):

    def __init__(self, secret, salt):
        self.serializer = URLSafeSerializer(get_plaintext(secret), salt=salt)

    def encode(self, content):
        return self.serializer.dumps(content)

    def decode(self, encoded_content):
        return self.serializer.loads(encoded_content)


@interface.implementer(IOAuthService)
class ProxyOAuthService(object):

    def __init__(self, authorization_url):
        self.authorization_url = authorization_url
        self.params = {}

    def _url_with_params(self, url, params):
        url_parts = list(urllib_parse.urlparse(url))
        query = dict(urllib_parse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urllib_parse.urlencode(params)
        return urllib_parse.urlunparse(url_parts)

    @property
    def _signer(self):
        return component.getUtility(IContentSigner)

    def _sign(self, content):
        return self._signer.encode(content)

    def authorization_request_uri(self,
                                  client_id,
                                  response_type,
                                  scope,
                                  state=None,
                                  redirect_uri=None,
                                  **extra_params):
        state = state or hashlib.sha256(os.urandom(1024)).hexdigest()
        params = {
            "client_id": client_id,
            "response_type": response_type,
            "scope": scope,
        }

        # Since we're proxying this through a portal, and we don't
        # want an open redirector, sign the redirect uri as part of
        # the state so it can be verified in the portal.
        if redirect_uri:
            params["state"] = self._sign({
                "state": state,
                "redirect_uri": redirect_uri
            })

        params.update(extra_params)

        self.params.update(params)

        return self._url_with_params(self.authorization_url, params)

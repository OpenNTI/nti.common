#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from zope import interface

from zope.schema import URI

from nti.schema.field import TextLine as ValidTextLine


class IAWSKey(interface.Interface):
    Grant = ValidTextLine(title=u"Grant type", required=False)
    Purpose = ValidTextLine(title=u"Key Purpose", required=True)
    BucketName = ValidTextLine(title=u"Bucket name", required=False)
    PublicAccessKey = ValidTextLine(title=u"Public Access Key", required=True)
    SecretAccessKey = ValidTextLine(title=u"Secret access Key", required=True)


class ILDAP(interface.Interface):
    ID = ValidTextLine(title=u"LDAP identifier", required=True)
    URL = ValidTextLine(title=u"LDAP URL", required=True)
    Username = ValidTextLine(title=u"Bind username", required=True)
    Password = ValidTextLine(title=u"Bind password flag", required=True)
    BaseDN = ValidTextLine(title=u"Base DN", required=False)
    BackupURL = ValidTextLine(title=u"Backup LDAP URL", required=False)


class IOAuthKeys(interface.Interface):
    APIKey = ValidTextLine(title=u"API Key", required=True)
    SecretKey = ValidTextLine(title=u"Secret Key", required=True)


class IContentSigner(interface.Interface):
    """
    Allow secure delivery of information that can be decoded and verified
    later, e.g. during proxy of an OAuth request in OAuth portal.
    """

    def encode(content):
        """
        Encode and sign content for later verification and decoding.
        :return:
        """

    def decode(encoded_content):
        """
        Decode the signed content.  Throws exception if signature doesn't match.
        :return:
        """


class IOAuthService(interface.Interface):

    AuthorizationEndpoint = URI(title=u"Authorization Endpoint",
                                description=u"URL for the authorization request")

    def authorization_request_uri(client_id=None,
                                  state=None,
                                  scope=None,
                                  redirect_uri=None,
                                  response_type=None,
                                  **extra_params
                                  ):
        """
        Build the URI for the initial OAuth authorization request.

        :return:
        """

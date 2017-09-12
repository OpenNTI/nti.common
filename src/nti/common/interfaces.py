#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from zope import interface

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

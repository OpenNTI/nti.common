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
    Bucket = ValidTextLine(title=u"Bucket name", required=False)
    Purpose = ValidTextLine(title=u"Key Purpose", required=True)
    PublicAccessKey = ValidTextLine(title=u"Public Access Key", required=True)
    SecretAccessKey = ValidTextLine(title=u"Secret access Key", required=True)

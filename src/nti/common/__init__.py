#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.common.gravatar import _AVATAR_SERVICES
from nti.common.gravatar import KNOWN_GRAVATAR_TYPES
from nti.common.gravatar import GENERATED_GRAVATAR_TYPES

from nti.common.gravatar import create_gravatar_url

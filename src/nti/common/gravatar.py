#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import hashlib
from six.moves import urllib_parse

from nti.common._compat import bytes_

logger = __import__('logging').getLogger(__name__)


_AVATAR_SERVICES = {
    'gravatar': {
        True: 'secure.gravatar.com',
        False: 'www.gravatar.com'
    },
    'libravatar': {
        True: 'seccdn.libravatar.org',
        False: 'cdn.libravatar.org'
    }
}

#: Constants identifying the various generated gravatar types
GENERATED_GRAVATAR_TYPES = ('retro', 'identicon', 'monsterid', 'wavatar')

#: Constants for all types of gravatars, generated or static
KNOWN_GRAVATAR_TYPES = GENERATED_GRAVATAR_TYPES + ('mm', '404')

DEFAULT_SIZE = 128
MYSTERY_MAN_URL = "https://www.gravatar.com/avatar/0?d=mm&s=%s" % DEFAULT_SIZE


def create_gravatar_url(username,
                        defaultGravatarType='mm',
                        secure=False,
                        size=DEFAULT_SIZE,
                        service='gravatar'):
    """
    Return a gravatar URL for the given username (which is assumed to be an email address).

    :keyword basestring defaultGravatarType: The gravatar type to use if no specific
            gravatar is available. Defaults to ``mm`` for mystery man. 
            See :data:`KNOWN_GRAVATAR_TYPES` for the options.
    :keyword bool secure: If ``True`` (default ``False``) HTTPS URL will be generated.
    :keyword int size: The pixel dimensions of the image, between 1 and 512. Default 128.

    :return: A gravatar URL for the given username. 
             See http://en.gravatar.com/site/implement/images/
    """
    username = bytes_(username.lower())
    md5str = hashlib.md5(username).hexdigest()
    scheme = 'https' if secure else 'http'
    netloc = _AVATAR_SERVICES[service][secure]
    path = '/avatar/' + md5str
    params = ''
    query = 's=%s&d=%s' % (size, defaultGravatarType)
    fragment = ''
    # pylint: disable=too-many-function-args
    result = urllib_parse.urlunparse((scheme, netloc, path, params, query, fragment))
    result = str(result)
    return result

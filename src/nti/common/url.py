#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from six.moves import urllib_parse

logger = __import__('logging').getLogger(__name__)


def safe_add_query_params(url, params):
    """
    Adds query params properly to a url

    :param url: The url to be updated
    :param params: The query params in a dictionary
    :return: The url with the query params safely added
    """
    url_parts = list(urllib_parse.urlparse(url))
    # Query params are in index 4
    query_params = dict(urllib_parse.parse_qsl(url_parts[4]))
    query_params.update(params)
    url_parts[4] = urllib_parse.urlencode(query_params)
    return urllib_parse.urlunparse(url_parts)

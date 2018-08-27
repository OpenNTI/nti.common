#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from six.moves import urllib_parse

logger = __import__('logging').getLogger(__name__)


def _urlencode(query_params):
    """
    The urllib_parse.urlencode function uses quote_plus when encoding query params
    This results in spaces being encoded as plus signs instead of percent encoded
    The web app prefers that these are percent encoded so we implement that here
    """
    l = []
    for k, v in query_params.items():
        k = urllib_parse.quote(str(k))
        v = urllib_parse.quote(str(v))
        l.append(k + '=' + v)
    return '&'.join(l)


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
    url_parts[4] = _urlencode(query_params)
    return urllib_parse.urlunparse(url_parts)

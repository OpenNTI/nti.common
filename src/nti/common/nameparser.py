#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=redefined-outer-name

from nameparser import HumanName

from nameparser.config import prefixes
from nameparser.config import suffixes
from nameparser.config import Constants

logger = __import__('logging').getLogger(__name__)


def suffix_acronyms():
    return suffixes.SUFFIX_ACRONYMS


def suffix_not_acronyms():
    return suffixes.SUFFIX_NOT_ACRONYMS


def get_suffixes():
    return suffix_acronyms() | suffix_not_acronyms()


def all_suffixes():
    return get_suffixes() | suffix_acronyms() | suffix_not_acronyms()


def all_prefixes():
    return prefixes.PREFIXES


def _create_constants(prefixes=(), extra_suffixes=(), emoji=False, use_titles=True):
    """
    Create a `Constants` object with our overrides.
    """
    not_acronyms = suffix_not_acronyms()
    acronyms = suffix_acronyms() | set(extra_suffixes)
    constants = Constants(prefixes=prefixes,
                          suffix_acronyms=acronyms,
                          suffix_not_acronyms=not_acronyms)
    if not use_titles:
        constants.titles = ()
    constants.regexes.emoji = emoji
    return constants

#: BWC
constants = _create_constants


def human_name(realname, prefixes=(), extra_suffixes=(), remove_emoji=False):
    """
    Returns a `HumanName` for the given realname.

    We are lenient here. If we have a `title` but not a proper first and last name,
    we will ignore titles.
    """
    constants = _create_constants(prefixes, extra_suffixes, emoji=remove_emoji)
    result = HumanName(realname, constants=constants)
    if result.title and (not result.first or not result.last):
        constants = _create_constants(prefixes, extra_suffixes,
                                      emoji=remove_emoji, use_titles=False)
        result = HumanName(realname, constants=constants)
    return result

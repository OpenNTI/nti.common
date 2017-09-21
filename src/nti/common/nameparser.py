#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

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


def constants(prefixes=(), extra_suffixes=(), emoji=False):
    not_acronyms = suffix_not_acronyms()
    acronyms = suffix_acronyms() | set(extra_suffixes)
    constants = Constants(prefixes=prefixes,
                          suffix_acronyms=acronyms,
                          suffix_not_acronyms=not_acronyms)
    try:
        constants.regexes.emoji = emoji
    except AttributeError:
        pass
    return constants


def human_name(realname, prefixes=(), extra_suffixes=(), remove_emoji=False):
    return HumanName(realname,
                     constants=constants(prefixes, extra_suffixes, emoji=remove_emoji))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import mimetypes as p_mimetypes

def _add_ngnix_types():
	p_mimetypes.add_type('text/html', '.shtml')
	p_mimetypes.add_type('text/mathml', '.mml')
	p_mimetypes.add_type('text/x-component', '.htc')
	p_mimetypes.add_type('image/x-jng', '.jng')
	p_mimetypes.add_type('application/java-archive', '.war')
	p_mimetypes.add_type('application/java-archive', '.ear')
	p_mimetypes.add_type('application/x-cocoa', '.cco')
	p_mimetypes.add_type('application/x-java-archive-diff', '.jardiff');
	p_mimetypes.add_type('application/x-makeself', '.run')
	p_mimetypes.add_type('application/x-perl', ',pm')
	p_mimetypes.add_type('application/x-redhat-package-manager', '.rpm')
	p_mimetypes.add_type('application/x-sea', '.sea')
	p_mimetypes.add_type('application/x-tcl', '.tcl')
	p_mimetypes.add_type('application/x-tcl', '.tk')
	p_mimetypes.add_type('application/x-x509-ca-cert', '.pem')
	p_mimetypes.add_type('video/3gpp', '.3gpp')
_add_ngnix_types()
del _add_ngnix_types

def guess_type(url, strict=True):
	return p_mimetypes.guess_type(url, strict)

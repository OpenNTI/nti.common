#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

def NoPickle(cls):
	"""
	A class decorator that prevents an object
	from being pickled. Useful for ensuring certain
	objects do not get pickled

	.. warning:: If you subclass something that used this
		decorator, you should override ``__reduce_ex__``
		(or both it and ``__reduce__``).
	"""

	msg = "Not allowed to pickle %s" % cls

	def __reduce_ex__(self, protocol):
		raise TypeError(msg)

	def __reduce__(self):
		return self.__reduce_ex__(0)

	cls.__reduce__ = __reduce__
	cls.__reduce_ex__ = __reduce_ex__

	return cls

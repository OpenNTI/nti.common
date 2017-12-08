#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import bz2
import gzip
import shutil
import tarfile
import zipfile
import tempfile

logger = __import__('logging').getLogger(__name__)


def is_archive(source, magic):
    if hasattr(source, "read"):
        source.seek(0)
        file_start = source.read(len(magic))
    else:
        with open(source, "rb") as fp:
            file_start = fp.read(len(magic))
    return file_start.startswith(magic)


def is_gzip(source):
    return is_archive(source, b"\x1f\x8b\x08")


def is_bz2(source):
    return is_archive(source, b"\x42\x5a\x68")


def extract_all(source):
    """
    Extract all members from the source file and returns
    the unarchived source or directory
    """
    if not os.path.isfile(source):
        return source
    if is_gzip(source):
        target, _ = os.path.splitext(source)
        with gzip.open(source, "rb") as f_in, open(target, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        return extract_all(target)
    elif is_bz2(source):
        target, _ = os.path.splitext(source)
        with bz2.BZ2File(source) as f_in, open(target, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        return extract_all(target)
    elif tarfile.is_tarfile(source):
        _, name = os.path.split(source)
        if name.lower().endswith('.tar'):
            name = name[:-4]
        target = os.path.join(tempfile.mkdtemp(), name)
        tar = tarfile.TarFile(source)
        tar.extractall(target)
        tar.close()
        files = os.listdir(target)
        if files and len(files) == 1:
            target = os.path.join(target, files[0])
        return extract_all(target)
    elif zipfile.is_zipfile(source):
        _, name = os.path.split(source)
        if name.lower().endswith('.zip'):
            name = name[:-4]
        target = os.path.join(tempfile.mkdtemp(), name)
        zf = zipfile.ZipFile(source)
        zf.extractall(target)
        zf.close()
        files = os.listdir(target)
        if files and len(files) == 1:
            target = os.path.join(target, files[0])
        return extract_all(target)
    else:
        return source
extractall = extract_all

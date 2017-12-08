#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that

import os
import bz2
import gzip
import shutil
import tarfile
import zipfile
import tempfile
from io import BytesIO

import unittest

from nti.common.io import is_bz2
from nti.common.io import is_gzip
from nti.common.io import extract_all

class TestIO(unittest.TestCase):

    data = b'ichigo and aizen'

    def test_is_gzip(self):
        bio = BytesIO()
        with gzip.GzipFile(fileobj=bio, mode="wb") as fp:
            fp.write(self.data)
        assert_that(is_gzip(bio), is_(True))

    def test_is_bz2(self):
        tmp_dir = tempfile.mkdtemp()
        try:
            out_name = os.path.join(tmp_dir, 'data.dat')
            with bz2.BZ2File(out_name, mode="wb") as fp:
                fp.write(self.data)
            assert_that(is_bz2(out_name), is_(True))
        finally:
            shutil.rmtree(tmp_dir, True)

    def test_extract_all(self):
        path = os.path.dirname(__file__)
        assert_that(extract_all(path), is_(path))

    def test_extract_all_tar_gz(self):
        tmp_dir = tempfile.mkdtemp()
        try:
            out_name = os.path.join(tmp_dir, "data.dat")
            with open(out_name, "wb") as fp:
                fp.write(self.data)
            tar_name = os.path.join(tmp_dir, 'data.tar.gz')
            with tarfile.open(tar_name, mode="w:gz") as fp:
                fp.add(out_name, arcname='data.tex')
            source = extract_all(tar_name)
            assert_that(source, is_not(none()))
            assert_that(os.path.isdir(source), is_(False))
            shutil.rmtree(source, True)
        finally:
            shutil.rmtree(tmp_dir, True)
            
    def test_extract_bz2(self):
        tmp_dir = tempfile.mkdtemp()
        try:
            out_name = os.path.join(tmp_dir, 'data.dat.bz2')
            with bz2.BZ2File(out_name, mode="wb") as fp:
                fp.write(self.data)
            source = extract_all(out_name)
            assert_that(source, is_not(none()))
            assert_that(os.path.isdir(source), is_(False))
            shutil.rmtree(source, True)
        finally:
            shutil.rmtree(tmp_dir, True)
            
    def test_extract_zip_file(self):
        tmp_dir = tempfile.mkdtemp()
        try:
            out_name = os.path.join(tmp_dir, 'data.zip')
            with zipfile.ZipFile(out_name, mode='w') as zf:
                zf.writestr('ichigo.txt', b'ichigo')
            source = extract_all(out_name)
            assert_that(source, is_not(none()))
            assert_that(os.path.isdir(source), is_(False))
            shutil.rmtree(source, True)
        finally:
            shutil.rmtree(tmp_dir, True)
    
    def test_extract_zip_dir(self):
        tmp_dir = tempfile.mkdtemp()
        try:
            out_name = os.path.join(tmp_dir, 'data.zip')
            with zipfile.ZipFile(out_name, mode='w') as zf:
                zf.writestr('aizen.txt', b'aizen')
                zf.writestr('ichigo.txt', b'ichigo')
            source = extract_all(out_name)
            assert_that(source, is_not(none()))
            assert_that(os.path.isdir(source), is_(True))
            shutil.rmtree(source, True)
        finally:
            shutil.rmtree(tmp_dir, True)

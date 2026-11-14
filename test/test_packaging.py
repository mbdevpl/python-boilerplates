"""Tests for packaging."""

import pathlib
import shutil
import unittest

from version_query import predict_version_str

import boilerplates.packaging_tests

import setup

VERSION = predict_version_str()
_HERE = pathlib.Path(__file__).parent


class Tests(boilerplates.packaging_tests.PackagingTests):

    version = VERSION


class SetupPyTests(unittest.TestCase):

    def test_prepare_local_version_query(self):
        path = _HERE.parent / 'boilerplates' / 'bundled_version_query'
        self.assertTrue(
            path.exists(), 'bundled version-query not found, please run "python -m build"')
        setup.prepare_local_version_query()
        self.assertTrue(path.exists())
        shutil.rmtree(path)
        self.assertFalse(path.exists())
        setup.prepare_local_version_query()
        self.assertTrue(path.exists())

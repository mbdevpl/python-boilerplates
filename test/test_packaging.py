"""Tests for packaging."""

from version_query import predict_version_str

import boilerplates.packaging_tests

VERSION = predict_version_str()


class Tests(boilerplates.packaging_tests.PackagingTests):

    version = VERSION

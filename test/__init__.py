"""Initialization of tests of boilerplates package."""

import logging

import boilerplates.logging


class TestsLogging(boilerplates.logging.Logging):
    """Logging configuration for tests."""

    packages = ['boilerplates']


TestsLogging.configure()

logging.getLogger('boilerplates.bundled_version_query').setLevel(logging.WARNING)

"""Initialization of tests of boilerplates package."""

import boilerplates.logging


class TestsLogging(boilerplates.logging.Logging):
    """Logging configuration for tests."""

    packages = ['boilerplates']


TestsLogging.configure()

"""Initialization of tests of boilerplates package."""

import logging

import boilerplates.logging


class TestsLogging(boilerplates.logging.Logging):
    """Logging configuration for tests."""

    packages = ['boilerplates']
    level_package = logging.DEBUG


TestsLogging.configure_basic()

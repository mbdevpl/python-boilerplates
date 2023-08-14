"""Tests for boilerplates.config module."""

import os
import pathlib
import tempfile
import unittest
import unittest.mock

import boilerplates.config


class UnitTests(unittest.TestCase):
    """Test basic functionalities of the config boilerplate."""

    def test_normalize_path(self):
        home_path = os.environ['HOME']
        self.assertEqual(boilerplates.config.normalize_path('~/folder'), f'{home_path}/folder')

        self.assertEqual(
            boilerplates.config.normalize_path(pathlib.Path('~', 'something')),
            pathlib.Path(home_path).joinpath('something'))

    def test_initialize_config_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with unittest.mock.patch.object(
                    boilerplates.config, 'CONFIG_PATH', pathlib.Path(temp_dir)):
                self.assertTrue(boilerplates.config.CONFIG_PATH.is_dir())
                boilerplates.config.initialize_config_directory('my_app')
                self.assertTrue(boilerplates.config.CONFIG_PATH.joinpath('my_app').is_dir())

            with unittest.mock.patch.object(
                    boilerplates.config, 'CONFIG_PATH', pathlib.Path(temp_dir, 'logs')):
                self.assertFalse(boilerplates.config.CONFIG_PATH.exists())
                boilerplates.config.initialize_config_directory('my_app')
                self.assertTrue(boilerplates.config.CONFIG_PATH.is_dir())
                self.assertTrue(boilerplates.config.CONFIG_PATH.joinpath('my_app').is_dir())

            pathlib.Path(temp_dir, 'logging').mkdir()
            with unittest.mock.patch.object(
                    boilerplates.config, 'CONFIG_PATH', pathlib.Path(temp_dir)):
                self.assertTrue(boilerplates.config.CONFIG_PATH.joinpath('logging').is_dir())
                boilerplates.config.initialize_config_directory('logging')
                self.assertTrue(boilerplates.config.CONFIG_PATH.joinpath('logging').is_dir())

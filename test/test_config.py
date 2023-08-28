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
        home_path = os.path.expanduser('~')
        self.assertEqual(boilerplates.config.normalize_path('~/folder'), f'{home_path}/folder')

        self.assertEqual(
            boilerplates.config.normalize_path(pathlib.Path('~', 'something')),
            pathlib.Path(home_path).joinpath('something'))

        envvar_value = 'my_custom_value'
        os.environ['MY_CUSTOM_VAR'] = envvar_value

        self.assertEqual(
            boilerplates.config.normalize_path(r'${MY_CUSTOM_VAR}/folder'),
            f'{envvar_value}/folder')

        self.assertEqual(
            boilerplates.config.normalize_path(pathlib.Path(r'${MY_CUSTOM_VAR}', 'something')),
            pathlib.Path(envvar_value).joinpath('something'))

    def test_initialize_config_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with unittest.mock.patch.object(
                    boilerplates.config, 'CONFIGS_PATH', pathlib.Path(temp_dir)):
                self.assertTrue(boilerplates.config.CONFIGS_PATH.is_dir())
                boilerplates.config.initialize_config_directory('my_app')
                self.assertTrue(boilerplates.config.CONFIGS_PATH.joinpath('my_app').is_dir())

            with unittest.mock.patch.object(
                    boilerplates.config, 'CONFIGS_PATH', pathlib.Path(temp_dir, 'logs')):
                self.assertFalse(boilerplates.config.CONFIGS_PATH.exists())
                boilerplates.config.initialize_config_directory('my_app')
                self.assertTrue(boilerplates.config.CONFIGS_PATH.is_dir())
                self.assertTrue(boilerplates.config.CONFIGS_PATH.joinpath('my_app').is_dir())

            pathlib.Path(temp_dir, 'logging').mkdir()
            with unittest.mock.patch.object(
                    boilerplates.config, 'CONFIGS_PATH', pathlib.Path(temp_dir)):
                self.assertTrue(boilerplates.config.CONFIGS_PATH.joinpath('logging').is_dir())
                boilerplates.config.initialize_config_directory('logging')
                self.assertTrue(boilerplates.config.CONFIGS_PATH.joinpath('logging').is_dir())

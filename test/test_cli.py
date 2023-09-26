"""Tests for the CLI boilerplate."""

import argparse
import contextlib
import logging
import os
import pathlib
import unittest

import boilerplates.cli


class UnitTests(unittest.TestCase):
    """Test basic functionalities of the CLI boilerplate."""

    def test_copyright_notice(self):
        notice = boilerplates.cli.make_copyright_notice(2020)
        self.assertTrue(notice.startswith('Copyright 2020 '), msg=notice)
        notice = boilerplates.cli.make_copyright_notice(2020, 2020)
        self.assertTrue(notice.startswith('Copyright 2020 '), msg=notice)
        notice = boilerplates.cli.make_copyright_notice(2020, 2023)
        self.assertTrue(notice.startswith('Copyright 2020-2023 '), msg=notice)

    def test_version_option(self):
        parser = argparse.ArgumentParser('boilerplates_cli_test')
        boilerplates.cli.add_version_option(parser, '1.0.0')
        with pathlib.Path(os.devnull).open('w', encoding='utf-8') as devnull:
            with contextlib.redirect_stderr(devnull):
                with self.assertRaises(SystemExit):
                    parser.parse_args(['--version'])

    def test_logging_level_conversion(self):
        for logging_level in (
                logging.NOTSET, logging.DEBUG, logging.WARNING, logging.ERROR, logging.CRITICAL):
            with self.subTest(logging_level=logging_level):
                verbosity = boilerplates.cli.logging_level_to_verbosity_level(logging_level)
                self.assertGreaterEqual(
                    verbosity,
                    boilerplates.cli._VERBOSITY_MIN)  # pylint: disable = protected-access
                self.assertLessEqual(
                    verbosity,
                    boilerplates.cli._VERBOSITY_MAX)  # pylint: disable = protected-access
                converted_logging_level = \
                    boilerplates.cli.verbosity_level_to_logging_level(verbosity)
                self.assertEqual(converted_logging_level, logging_level)

    def test_verbosity_level_conversion(self):
        for verbosity in range(-10, 10):
            with self.subTest(verbosity=verbosity):
                logging_level = boilerplates.cli.verbosity_level_to_logging_level(verbosity)
                converted_verbosity = \
                    boilerplates.cli.logging_level_to_verbosity_level(logging_level)
                self.assertEqual(converted_verbosity, verbosity)

    def test_verbosity_default(self):
        parser = argparse.ArgumentParser()
        boilerplates.cli.add_verbosity_group(parser)
        parsed_args = parser.parse_args([])
        verbosity = boilerplates.cli.get_verbosity_level(parsed_args)
        self.assertEqual(
            verbosity, boilerplates.cli._VERBOSITY_DEFAULT)  # pylint: disable = protected-access

    def test_verbosity_by_level(self):
        parser = argparse.ArgumentParser()
        boilerplates.cli.add_verbosity_group(parser)
        for verbosity in range(
                boilerplates.cli._VERBOSITY_MIN,  # pylint: disable = protected-access
                boilerplates.cli._VERBOSITY_MAX):  # pylint: disable = protected-access
            parsed_args = parser.parse_args([f'--verbosity={verbosity}'])
            parsed_verbosity = boilerplates.cli.get_verbosity_level(parsed_args)
            self.assertEqual(parsed_verbosity, verbosity)
            logging_level = boilerplates.cli.get_logging_level(parsed_args)
            self.assertEqual(
                logging_level, boilerplates.cli.verbosity_level_to_logging_level(verbosity))

    def test_verbosity_by_flags(self):
        parser = argparse.ArgumentParser()
        boilerplates.cli.add_verbosity_group(parser)
        for flags, verbosity_change, in {
                ('-v',): 1,
                ('--verbose',): 1,
                ('-v', '-v'): 2,
                ('-vv',): 2,
                ('-q',): -1,
                ('--quiet',): -1,
                ('-q', '-q'): -2,
                ('-qq',): -2
                }.items():
            parsed_args = parser.parse_args(flags)
            verbosity = boilerplates.cli.get_verbosity_level(parsed_args)
            # pylint: disable = protected-access
            self.assertEqual(verbosity, boilerplates.cli._VERBOSITY_DEFAULT + verbosity_change)

    def test_too_many_verbosity_flags(self):
        parser = argparse.ArgumentParser()
        boilerplates.cli.add_verbosity_group(parser)
        # pylint: disable = protected-access
        for flags in (
                [f'-{"v" * (boilerplates.cli._VERBOSE_MAX_COUNT + 1)}'],
                [f'-{"v" * (boilerplates.cli._VERBOSE_MAX_COUNT + 2)}'],
                [f'-{"q" * (boilerplates.cli._QUIET_MAX_COUNT + 1)}'],
                [f'-{"q" * (boilerplates.cli._QUIET_MAX_COUNT + 2)}']):
            parsed_args = parser.parse_args(flags)
            with self.assertRaises(ValueError):
                boilerplates.cli.get_verbosity_level(parsed_args)

    def test_dedent_except_first_line(self):
        self.assertEqual(
            boilerplates.cli.dedent_except_first_line('  test'), '  test')
        self.assertEqual(
            boilerplates.cli.dedent_except_first_line('  test\n  test'), '  test\ntest')

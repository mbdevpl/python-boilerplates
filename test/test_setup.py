"""Tests for boilerplates.setup module."""

import itertools
import logging
import os
import pathlib
import tempfile
import unittest

import boilerplates.setup

_LOG = logging.getLogger(__name__)


CLASSIFIERS_LICENSES = (
    'License :: OSI Approved :: Python License (CNRI Python License)',
    'License :: OSI Approved :: Python Software Foundation License',
    'License :: Other/Proprietary License',
    'License :: Public Domain')

CLASSIFIERS_PYTHON_VERSIONS = tuple("""Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.0
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3 :: Only""".splitlines())

CLASSIFIERS_PYTHON_IMPLEMENTATIONS = tuple("""Programming Language :: Python :: Implementation
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: Jython
Programming Language :: Python :: Implementation :: PyPy
Programming Language :: Python :: Implementation :: Stackless""".splitlines())

CLASSIFIERS_VARIOUS = (
    'Framework :: IPython',
    'Topic :: Scientific/Engineering',
    'Topic :: Sociology',
    'Topic :: Security :: Cryptography',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Version Control :: Git',
    'Topic :: System',
    'Topic :: Utilities')

CLASSIFIERS_LICENSES_TUPLES = tuple((_,) for _ in CLASSIFIERS_LICENSES) + ((),)

CLASSIFIERS_PYTHON_VERSIONS_COMBINATIONS = tuple((_,) for _ in CLASSIFIERS_PYTHON_VERSIONS)

CLASSIFIERS_PYTHON_IMPLEMENTATIONS_TUPLES = tuple((_,) for _ in CLASSIFIERS_PYTHON_IMPLEMENTATIONS)

CLASSIFIERS_VARIOUS_COMBINATIONS = tuple(itertools.combinations(
    CLASSIFIERS_VARIOUS, len(CLASSIFIERS_VARIOUS) - 1)) + (CLASSIFIERS_VARIOUS,)

ALL_CLASSIFIERS_VARIANTS = [
    licenses + versions + implementations + various
    for licenses in CLASSIFIERS_LICENSES_TUPLES
    for versions in CLASSIFIERS_PYTHON_VERSIONS_COMBINATIONS
    for implementations in CLASSIFIERS_PYTHON_IMPLEMENTATIONS_TUPLES
    for various in CLASSIFIERS_VARIOUS_COMBINATIONS]

LINK_EXAMPLES = [
    (None, 'setup.py', True), ('this file', 'setup.py', True), (None, 'test/test_setup.py', True),
    (None, 'test/test_setup.py#L98', True), ('line 5 of this file', 'setup.py#L5', True),
    (None, 'http://site.com', False), (None, '../something/else', False), (None, 'no.thing', False),
    (None, '/my/abs/path', False), ('test dir', 'test', True)]


class UnitTests(unittest.TestCase):
    """Test basic functionalities of the setup boilerplate."""

    def test_find_version(self):
        result = boilerplates.setup.find_version('.', 'setup')
        self.assertIsInstance(result, str)

    def test_find_packages(self):
        results = boilerplates.setup.find_packages()
        self.assertIsInstance(results, list)
        for result in results:
            self.assertIsInstance(result, str)

    def test_requirements(self):
        results = boilerplates.setup.parse_requirements()
        self.assertIsInstance(results, list)
        self.assertTrue(all(isinstance(result, str) for result in results), msg=results)

    def test_requirements_nested(self):
        results = boilerplates.setup.parse_requirements('requirements_test.txt')
        self.assertIsInstance(results, list)
        self.assertTrue(all(isinstance(result, str) for result in results), msg=results)

    def test_requirements_empty(self):
        with tempfile.NamedTemporaryFile('w', delete=False) as reqs_file:
            pass
        results = boilerplates.setup.parse_requirements(reqs_file.name)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)
        os.remove(reqs_file.name)

    def test_requirements_comments(self):
        reqs = ['# comment', 'numpy', '', '# another comment', 'scipy', '', '# one more comment']
        with tempfile.NamedTemporaryFile('w', delete=False) as reqs_file:
            for req in reqs:
                print(req, file=reqs_file)
        results = boilerplates.setup.parse_requirements(reqs_file.name)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertLess(len(results), len(reqs))
        os.remove(reqs_file.name)

    def test_python_versions(self):
        for variant in ALL_CLASSIFIERS_VARIANTS:
            with self.subTest(variant=variant):
                result = boilerplates.setup.find_required_python_version(variant)
                if result is not None:
                    self.assertIsInstance(result, str)

    def test_python_versions_combined(self):
        classifiers = [
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.5']
        req = boilerplates.setup.find_required_python_version(classifiers)
        self.assertEqual(req, '>=3.5')

    def test_python_versions_reversed(self):
        classifiers = [
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6']
        req = boilerplates.setup.find_required_python_version(classifiers)
        self.assertEqual(req, '>=3.4')
        req = boilerplates.setup.find_required_python_version(reversed(classifiers))
        self.assertEqual(req, '>=3.4')

    def test_python_versions_none(self):
        result = boilerplates.setup.find_required_python_version([])
        self.assertIsNone(result)

    def test_python_versions_many_only(self):
        classifiers = [
            'Programming Language :: Python :: 2 :: Only',
            'Programming Language :: Python :: 3 :: Only']
        with self.assertRaises(ValueError):
            boilerplates.setup.find_required_python_version(classifiers)

    def test_python_versions_conflict(self):
        classifier_variants = [
            ['Programming Language :: Python :: 2.7',
             'Programming Language :: Python :: 3 :: Only'],
            ['Programming Language :: Python :: 2 :: Only',
             'Programming Language :: Python :: 3.0']]
        for classifiers in classifier_variants:
            with self.assertRaises(ValueError):
                boilerplates.setup.find_required_python_version(classifiers)


class PackageTests(unittest.TestCase):
    """Test methods of Package class."""

    def test_try_fields(self):
        class Package(boilerplates.setup.Package):  # pylint: disable = too-few-public-methods
            name = 'package name'
            description = 'package description'

        self.assertEqual(Package.try_fields('name', 'description'), 'package name')
        self.assertEqual(Package.try_fields('bad_field', 'description'), 'package description')
        with self.assertRaises(AttributeError):
            self.assertIsNone(Package.try_fields())
        with self.assertRaises(AttributeError):
            Package.try_fields('bad_field', 'another_bad_field')

    def test_parse_readme(self):
        class Package(boilerplates.setup.Package):  # pylint: disable = too-few-public-methods
            name = 'package name'
            description = 'package description'
            version = '1.2.3.4'
            url = 'https://github.com/example'

        with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False) as temp_file:
            temp_file.write('test test test')
        result, content_type = Package.parse_readme(temp_file.name)
        os.remove(temp_file.name)
        self.assertIsInstance(result, str)
        self.assertIsInstance(content_type, str)

        prefix = 'https://github.com/example/blob/v1.2.3.4/'
        for name, link, done in LINK_EXAMPLES:
            name = '' if name is None else name + ' '
            text = f'Please see `{name}<{link}>`_ for details.'
            with tempfile.TemporaryDirectory() as temp_folder:
                with tempfile.NamedTemporaryFile(
                        'w', dir=temp_folder, suffix='.rst', delete=False) as temp_file:
                    temp_file.write(text)
                pathlib.Path(temp_folder, 'setup.py').touch()
                pathlib.Path(temp_folder, 'test').mkdir()
                pathlib.Path(temp_folder, 'test', 'test_setup.py').touch()
                result, content_type = Package.parse_readme(temp_file.name)
                os.remove(temp_file.name)
            self.assertIsInstance(result, str)
            self.assertIsInstance(content_type, str)
            if not done:
                self.assertEqual(result, text)
                continue
            if name == '':
                name = link + ' '
            self.assertIn(f'`{name}<{prefix}{link}>`_', result)

    def test_prepare(self):
        version_ = '1.2.3.4.5.6.7'
        long_description_ = 'long package description'

        class Package(boilerplates.setup.Package):
            # pylint: disable = too-few-public-methods, missing-docstring
            name = 'package name'
            version = version_
            description = 'package description'
            long_description = long_description_
            packages = []
            install_requires = []
            python_requires = ''

        self.assertEqual(Package.version, version_)
        self.assertEqual(Package.long_description, long_description_)
        Package.prepare()
        self.assertEqual(Package.version, version_)
        self.assertEqual(Package.long_description, long_description_)

        del Package.long_description
        del Package.packages
        del Package.install_requires
        del Package.python_requires
        Package.prepare()

        del Package.version
        with self.assertRaises(FileNotFoundError):
            Package.prepare()

    def test_prepare_license_files(self):
        # pylint: disable = protected-access

        class Package(boilerplates.setup.Package):
            name = 'package name'
            version = '0.1.0'

        self.assertIsNone(Package._existing_license_file_patterns)
        Package.prepare()
        self.assertIsNotNone(Package._existing_license_file_patterns)
        assert Package._existing_license_file_patterns is not None
        self.assertGreater(len(Package._existing_license_file_patterns), 0)

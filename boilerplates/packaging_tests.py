"""Test definitions for package building."""

import contextlib
import importlib
import io
import logging
import os
import pathlib
import runpy
import subprocess
import sys
import tempfile
import types
import typing as t
import unittest

from .setup import find_version

_LOG = logging.getLogger(__name__)


def expand_args_by_globbing_items(
        *args: str, cwd: t.Optional[pathlib.Path] = None) -> t.Tuple[str, ...]:
    """Expand a list of glob expressions."""
    if cwd is None:
        cwd = pathlib.Path.cwd()
    expanded_args = []
    for arg in args:
        if '*' not in arg:
            expanded_args.append(arg)
            continue
        expanded_arg = [str(_.relative_to(cwd)) for _ in cwd.glob(arg)]
        assert expanded_arg, arg
        _LOG.debug('expanded arg "%s" to %s', arg, expanded_arg)
        expanded_args += expanded_arg
    _LOG.debug('expanded args to %s', expanded_args)
    return tuple(expanded_args)


def run_program(*args, glob: bool = False) -> None:
    """Run subprocess with given args. Use path globbing for each arg that contains an asterisk."""
    if glob:
        args = expand_args_by_globbing_items(*args)
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as err:
        raise AssertionError(f'execution of {args} failed') from err


def run_pip(*args, **kwargs) -> None:
    run_program(sys.executable, '-m', 'pip', *args, **kwargs)


def run_module(name: str, *args, run_name: str = '__main__') -> None:
    backup_sys_argv = sys.argv
    sys.argv = [name + '.py'] + list(args)
    runpy.run_module(name, run_name=run_name)
    sys.argv = backup_sys_argv


def import_module(name: str = 'setup') -> types.ModuleType:
    setup_module = importlib.import_module(name)
    return setup_module


def import_module_member(module_name: str, member_name: str) -> t.Any:
    module = import_module(module_name)
    return getattr(module, member_name)


def get_package_folder_name():
    """Attempt to guess the built package name."""
    name_from_setup = import_module_member('setup', 'Package').name.replace('-', '_')
    cwd = pathlib.Path.cwd()
    directories = [
        path for path in cwd.iterdir() if pathlib.Path(cwd, path).is_dir()
        and pathlib.Path(cwd, path, '__init__.py').is_file() and path.name != 'test']
    directory_names = {_.name for _ in directories}
    assert name_from_setup in directory_names, directories
    return name_from_setup


@unittest.skipUnless(os.environ.get('TEST_PACKAGING') or os.environ.get('CI'),
                     'skipping packaging tests for actual package')
class PackagingTests(unittest.TestCase):
    """Test if the boilerplate can actually create a valid package."""

    pkg_name: t.Optional[str] = None
    version: t.Optional[str] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pkg_name = get_package_folder_name() if cls.pkg_name is None else cls.pkg_name
        cls.version = find_version(cls.pkg_name) if cls.version is None else cls.version

    def test_expand_args_in_cwd(self):
        expanded_args = expand_args_by_globbing_items('*.py')
        self.assertIn('setup.py', expanded_args)

    def test_expand_args_in_package_folder(self):
        expanded_args = expand_args_by_globbing_items('*.py', cwd=pathlib.Path(self.pkg_name))
        self.assertIn('__init__.py', expanded_args)

    def test_setup_help(self):
        stdout_buffer = io.StringIO()
        with contextlib.redirect_stdout(stdout_buffer):
            run_module('setup', '--help')
        self.assertIn('usage: setup.py', stdout_buffer.getvalue())

    def test_build(self):
        run_program(sys.executable, '-m', 'build')
        self.assertTrue(os.path.isdir('dist'))

    def test_build_wheel(self):
        run_module('build', '--wheel')
        self.assertTrue(os.path.isdir('dist'))

    def test_build_wheel_no_isolation(self):
        run_module('build', '--wheel', '--no-isolation')
        self.assertTrue(os.path.isdir('dist'))

    def test_build_source(self):
        run_module('build', '--sdist')
        self.assertTrue(os.path.isdir('dist'))

    def test_build_source_no_isolation(self):
        run_module('build', '--sdist', '--no-isolation')
        self.assertTrue(os.path.isdir('dist'))

    def test_install_code(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            run_pip('install', '--ignore-installed', '--prefix', temporary_folder, '.')
        self.assertFalse(pathlib.Path(temporary_folder).exists())

    def test_install_source_tar(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            run_pip(
                'install', '--ignore-installed', '--prefix', temporary_folder,
                f'dist/*-{self.version}.tar.gz', glob=True)
        self.assertFalse(pathlib.Path(temporary_folder).exists())

    def test_install_wheel(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            run_pip(
                'install', '--ignore-installed', '--prefix', temporary_folder,
                f'dist/*-{self.version}-*.whl', glob=True)
        self.assertFalse(pathlib.Path(temporary_folder).exists())

    def test_pip_error(self):
        with self.assertRaises(AssertionError):
            run_pip('wrong_pip_command')

    def test_setup_do_nothing_or_error(self):
        run_module('setup', 'wrong_setup_command', run_name='__not_main__')
        with self.assertRaises(SystemExit):
            run_module('setup', 'wrong_setup_command')

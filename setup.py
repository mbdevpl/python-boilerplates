"""Setup script for boilerplates package."""

import pathlib
import shutil
import tempfile

import git

import boilerplates.setup


def prepare_local_version_query():
    """Prepare local copy of version_query package to avoid circular dependency between packages."""
    here = pathlib.Path(__file__).parent
    module_path = here / 'boilerplates' / 'bundled_version_query'
    if module_path.exists():
        return
    with tempfile.TemporaryDirectory() as temporary_path:
        repo_path = pathlib.Path(temporary_path)
        print(f'ensuring version-query repository is available locally at "{repo_path}"')
        repo = git.Repo.clone_from('https://github.com/mbdevpl/version-query', repo_path)
        repo.git.checkout('v1.6.3')
        print(f'ensuring version_query module is available locally at "{module_path}"')
        shutil.copytree(repo_path / 'version_query', module_path, dirs_exist_ok=True)
    for filename in ('_version.py', '__main__.py', 'main.py'):
        module_path.joinpath(filename).unlink()


prepare_local_version_query()

# pylint: disable = wrong-import-position
from boilerplates.bundled_version_query import predict_version_str  # noqa: E402

VERSION = predict_version_str()


class Package(boilerplates.setup.Package):
    """Package metadata."""

    name = 'boilerplates'
    version = VERSION
    description = 'Various boilerplates used in almost all of my Python packages.'
    url = 'https://github.com/mbdevpl/python-boilerplates'
    author = 'Mateusz Bysiek, Stian Hanssen'
    maintainer = 'Mateusz Bysiek'
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Logging',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
        'Typing :: Typed']
    keywords = ['git', 'logging', 'packaging', 'releasing']
    extras_require = {
        'setup': boilerplates.setup.parse_requirements('requirements_setup.txt'),
        'packaging-tests': boilerplates.setup.parse_requirements(
            'requirements_packaging_tests.txt'),
        'config': boilerplates.setup.parse_requirements('requirements_config.txt'),
        'logging': boilerplates.setup.parse_requirements('requirements_logging.txt'),
        'sentry': boilerplates.setup.parse_requirements('requirements_sentry.txt'),
        'cli': boilerplates.setup.parse_requirements('requirements_cli.txt'),
        'git-repo-tests': boilerplates.setup.parse_requirements('requirements_git_repo_tests.txt')}


if __name__ == '__main__':
    Package.setup()

"""Setup script for boilerplates package."""

import pathlib
import shutil
import sys
import tempfile

import git

_HERE = pathlib.Path(__file__).parent


def prepare_local_version_query() -> None:
    """Prepare local copy of version_query package to avoid circular dependency between packages."""
    module_path = _HERE / 'boilerplates' / 'bundled_version_query'
    if module_path.exists():
        return
    with tempfile.TemporaryDirectory() as temporary_path:
        repo_path = pathlib.Path(temporary_path)
        print(f'ensuring version-query repository is available locally at "{repo_path}"')
        repo = git.Repo.clone_from('https://github.com/mbdevpl/version-query', repo_path)
        repo.git.checkout('v1.8.0')
        print(f'ensuring version_query module is available locally at "{module_path}"')
        shutil.copytree(repo_path / 'version_query', module_path, dirs_exist_ok=True)
    for filename in ('_version.py', '__main__.py', 'main.py'):
        module_path.joinpath(filename).unlink()


def allow_local_boilerplates() -> None:
    """Add folder of this setup.py to Python path to use packaged code when building the package."""
    sys.path.insert(0, str(_HERE))


if __name__ == '__main__':
    prepare_local_version_query()
    allow_local_boilerplates()

# pylint: disable = wrong-import-position
import boilerplates.setup  # noqa: E402

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
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: 3.15',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Logging',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
        'Typing :: Typed']
    install_requires = []
    extras_require = {}


if __name__ == '__main__':
    Package.setup()

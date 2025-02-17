"""Setup script for boilerplates package."""

from version_query import predict_version_str

import boilerplates.setup

VERSION = predict_version_str()


class Package(boilerplates.setup.Package):
    """Package metadata."""

    name = 'boilerplates'
    version = VERSION
    description = 'Various boilerplates used in almost all of my Python packages.'
    url = 'https://github.com/mbdevpl/python-boilerplates'
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
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
        'packaging_tests': boilerplates.setup.parse_requirements(
            'requirements_packaging_tests.txt'),
        'config': boilerplates.setup.parse_requirements('requirements_config.txt'),
        'logging': boilerplates.setup.parse_requirements('requirements_logging.txt'),
        'sentry': boilerplates.setup.parse_requirements('requirements_sentry.txt'),
        'cli': boilerplates.setup.parse_requirements('requirements_cli.txt'),
        'git_repo_tests': boilerplates.setup.parse_requirements('requirements_git_repo_tests.txt')}


if __name__ == '__main__':
    Package.setup()

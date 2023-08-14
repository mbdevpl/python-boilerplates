"""Setup script for boilerplates package."""

import boilerplates.setup


class Package(boilerplates.setup.Package):
    """Package metadata."""

    name = 'boilerplates'
    description = 'Various boilerplates used in almost all of my Python packages.'
    url = 'https://github.com/mbdevpl/python-boilerplates'
    classifiers = [
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only']
    keywords = []
    extras_require = {
        'setup': boilerplates.setup.parse_requirements('requirements_setup.txt'),
        'packaging_tests': boilerplates.setup.parse_requirements(
            'requirements_packaging_tests.txt'),
        'config': boilerplates.setup.parse_requirements('requirements_config.txt')
    }


if __name__ == '__main__':
    Package.setup()

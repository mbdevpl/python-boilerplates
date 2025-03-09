.. role:: python(code)
    :language: python

.. role:: toml(code)
    :language: toml

===================
Python boilerplates
===================

Various boilerplates used in almost all of my Python packages.

.. image:: https://img.shields.io/pypi/v/boilerplates.svg
    :target: https://pypi.org/project/boilerplates
    :alt: package version from PyPI

.. image:: https://github.com/mbdevpl/python-boilerplates/actions/workflows/python.yml/badge.svg?branch=main
    :target: https://github.com/mbdevpl/python-boilerplates/actions
    :alt: build status from GitHub

.. image:: https://codecov.io/gh/mbdevpl/python-boilerplates/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/mbdevpl/python-boilerplates
    :alt: test coverage from Codecov

.. image:: https://api.codacy.com/project/badge/Grade/f22939bf833e40b89833d96c859bd7a4
    :target: https://app.codacy.com/gh/mbdevpl/python-boilerplates
    :alt: grade from Codacy

.. image:: https://img.shields.io/github/license/mbdevpl/python-boilerplates.svg
    :target: NOTICE
    :alt: license

This package includes boilerplates for various common tasks in Python packages, such as building
the package, testing the packaging process, storing the package config, logging for the package
or creating a CLI.

.. contents::
    :backlinks: none

Requirements
============

Python version 3.9 or later.

Python libraries as specified in `<requirements.txt>`_.

Building and running tests additionally requires packages listed in `<requirements_test.txt>`_.

Tested on Linux, macOS and Windows.

Available boilerplates
======================

Setup boilerplate
-----------------

Module ``boilerplates.setup`` provides a class ``Package`` that abstracts out
many of the common tasks needed to set up the package. The class has a
``setup()`` class method that can be called from the ``if __name__ == '__main__'`` block
in your ``setup.py`` file.

To avoid setup script boilerplate, create ``setup.py`` file with the minimal contents as given
below and modify it according to the specifics of your package.

See the implementation of ``boilerplates.setup.Package`` for all other available options.
Some fields don't need to be entered and will be automatically initialised using various detectors.
Also, some fields have default values.
See ``DEFAULT_*`` constants in the ``boilerplates.setup`` for those values.

Example ``setup.py``:

.. code:: python

    """Setup script."""

    import boilerplates.setup


    class Package(boilerplates.setup.Package):
        """Package metadata."""

        name = ''
        description = ''
        url = 'https://github.com/mbdevpl/...'
        author = '...'
        author_email = '...'
        classifiers = [
            'Development Status :: 1 - Planning',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3 :: Only']
        keywords = []


    if __name__ == '__main__':
        Package.setup()

You will also need the following in your ``pyproject.toml`` file:

.. code:: toml

    [build-system]
    requires = ['boilerplates[setup] ~= <version>']

Packaging tests
~~~~~~~~~~~~~~~

As an extension of setup boilerplate, there's an extra boilerplate for testing the packaging process,
in a way that enables 100% code coverage, including the ``setup.py`` script.

In order to use it, all you need to do is create a file as follows in your tests directory.

Example ``test/test_packaging.py``:

.. code:: python

    """Tests for packaging."""

    import boilerplates.packaging_tests


    class Tests(boilerplates.packaging_tests.PackagingTests):
        pass

And, you will need to add the following to your ``requirements_test.txt`` file (or equivalent):

.. code:: text

    boilerplates[packaging-tests] ~= <version>

Config boilerplate
------------------

Module ``boilerplates.config`` provides few utility functions useful to handle local configuration.

Example usage:

.. code:: python

    import boilerplates.config

    ...

    boilerplates.config.initialize_config_directory('app_name')

And, you will need to add the following to your ``requirements.txt`` file (or equivalent):

.. code:: text

    boilerplates[config] ~= <version>

Logging boilerplate
-------------------

Assumptions for this boilerplate are that you want to use the standard built-in Python
logging module (``logging``), and that your application probably has a CLI entry point
or some executable script, as opposed to only being a library.

To reduce boilerplate necessary to setup logging for such application,
add the following in your ``__main__.py``:

.. code:: python

    """Entry point of the command-line interface."""

    import boilerplates.logging


    class Logging(boilerplates.logging.Logging):
        """Logging configuration."""

        packages = ['package_name']


    ...


    if __name__ == '__main__':
        Logging.configure()
        ...

More advanced usage could be (just changing the ``Logging`` class definition):

.. code:: python

    class Logging(boilerplates.logging.Logging):
        """Logging configuration."""

        packages = ['package_name']
        level_global = logging.INFO
        enable_file = True
        directory = 'package_name'

You can and should adjust the class fields to your needs, please take a look
at the ``boilerplates.logging.Logging`` class implementation for details.

You may also use this boilerplate in tests even if your code is just a library. In such case,
add the following to your ``test/__init__.py``:

.. code:: python

    """Initialization of tests."""

    import logging

    import boilerplates.logging


    class TestsLogging(boilerplates.logging.Logging):
        """Logging configuration for tests."""

        packages = ['package_name']
        level_global = logging.INFO


    TestsLogging.configure()

If you wish, you can make your test logging config be a variant of your application logging config,
like so:

.. code:: python

    """Initialization of tests."""

    from my_package.__main__ import Logging


    class TestsLogging(Logging):
        """Logging configuration for tests."""

        level_global = logging.DEBUG  # relevant if level_global is set to e.g. INFO in parent class
        enable_file = False  # relevant if enable_file is set to True in parent class

As for using the logging in your code, you can use it as usual, for example:

.. code:: python

    # in a standalone script:
    _LOG = logging.getLogger(pathlib.Path(__file__).stem)
    # in a standalone script that can also be imported:
    _LOG = logging.getLogger(pathlib.Path(__file__).stem if __name__ == '__main__' else __name__)
    # in __main__.py:
    _LOG = logging.getLogger(pathlib.Path(__file__).parent.name)
    # in usual module files:
    _LOG = logging.getLogger(__name__)

And, you will need to add the following to your ``requirements.txt`` file (or equivalent):

.. code:: text

    boilerplates[logging] ~= <version>

Sentry boilerplate
------------------

This boilerplate aims at simplifying the process of setting up Sentry integration
for your Python application.

Assumptions for this boilerplate are similar to logging boilerplate, in that
you want to use the standard built-in Python
logging module (``logging``), and that your application probably has a CLI entry point
or some executable script, as opposed to only being a library.

Then, the example ``__main__.py`` file may look like:

.. code:: python

    """Entry point of the command-line interface."""

    import boilerplates.sentry

    from ._version import VERSION


    class Sentry(boilerplates.sentry.Sentry):
        """Sentry configuration."""

        release = VERSION


    ...


    if __name__ == '__main__':
        Sentry.init()
        ...

You can and should adjust the class fields to your needs, please take a look
at the ``boilerplates.sentry.Sentry`` class implementation for details.

And, you will need to add the following to your ``requirements.txt`` file (or equivalent):

.. code:: text

    boilerplates[sentry] ~= <version>

CLI boilerplate
---------------

This boilerplate aims at making CLIs easier to write, by providing a few utility functions.

Your example ``cli.py`` file which defines your command-line interface may look like:

.. code:: python

    """Command-line interface definition."""

    import argparse

    import boilerplates.cli

    def main(args=None):
        """Entry point of the command-line interface."""
        parser = argparse.ArgumentParser(
            prog='my-cli',
            description='''My command-line interface.''',
            epilog=boilerplates.cli.make_copyright_notice(
                2019, 2023, author='The Author', license_name='Apache License 2.0',
                url='https://github.com/...'))

        boilerplates.cli.add_version_option(parser, '1.0.1')
        boilerplates.cli.add_verbosity_group(parser)

        parsed_args = parser.parse_args(args)

        verbosity = boilerplates.cli.get_verbosity_level(parsed_args)
        ...

You can see the above example in action in the `<examples.ipynb>`_ notebook.
Please see the ``boilerplates.cli`` module for details of the available features.

And then, an example ``__main__.py`` file may look like:

.. code:: python

    """Entry point of the command-line interface."""

    # PYTHON_ARGCOMPLETE_OK

    from my_package import cli


    if __name__ == '__main__':
        cli.main()

And, you will need to add the following to your ``requirements.txt`` file (or equivalent):

.. code:: text

    boilerplates[cli] ~= <version>

Then, the output of running ``python -m my_package -h`` will look like:

.. code:: text

    usage: my-cli [-h] [--version] [--verbose | --quiet | --verbosity LEVEL]

    My command-line interface.

    options:
    -h, --help         show this help message and exit
    --version          show program's version number and exit
    --verbose, -v      be more verbose than by default (repeat up to 3 times for
                        stronger effect)
    --quiet, -q        be more quiet than by default (repeat up to 2 times for
                        stronger effect)
    --verbosity LEVEL  set verbosity level explicitly (normally from 0 to 5)

    Copyright 2019-2023 by The Author. Apache License 2.0. https://github.com/...

And the output of running ``python -m my_package --version`` will look like:

.. code:: text

    my-cli 1.0.1, Python 3.11.0 (main, Feb 13 2023, 00:02:15) [GCC 12.1.0]

Git repo tests boilerplate
--------------------------

This boilerplate aims at making it easier to test your package in a context of a git repository.

It's only useful if you create a Python package that operates on git repositories, and helps to
create and modify synthetic git repositories for testing purposes.

To start using ``boilerplates.git_repo_tests``, you can start with a file like this
in your test folder, for example ``test/test_with_git_repo.py``:

.. code:: python

    """Perform tests on and in synthetic git repositories."""

    import pathlib

    import boilerplates.git_repo_tests


    class Tests(boilerplates.git_repo_tests.GitRepoTests):

        ...

However, you will need to check the ``boilerplates.git_repo_tests.GitRepoTests`` class
for details of available features.

And, you will need to add the following to your ``requirements_test.txt`` file (or equivalent):

.. code:: text

    boilerplates[git-repo-tests] ~= <version>

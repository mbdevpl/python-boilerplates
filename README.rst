.. role:: python(code)
    :language: python

.. role:: toml(code)
    :language: toml

===================
Python boilerplates
===================

Various boilerplates used in almost all of my Python packages.

.. image:: https://img.shields.io/github/license/mbdevpl/python-boilerplates.svg
    :target: NOTICE
    :alt: license

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

This package includes boilerplates for various common tasks in Python packages, such as building
the package, testing the packaging process and storing the package config.

.. contents::
    :backlinks: none

Requirements
============

Python version 3.8 or later.

Python libraries as specified in `<requirements.txt>`_.

Building and running tests additionally requires packages listed in `<requirements_test.txt>`_.

Tested on Linux, OS X and Windows.

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
            'Programming Language :: Python :: 3.8',
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
    requires = ['boilerplates[setup] ~= 0.1']

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

    boilerplates[packaging_tests] ~= 0.1

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

    boilerplates[config] ~= 0.2

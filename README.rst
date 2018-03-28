====================
sphinxcontrib-apidoc
====================

.. image:: https://travis-ci.org/sphinx-contrib/apidoc.svg?branch=master
    :target: https://travis-ci.org/sphinx-contrib/apidoc

A Sphinx extension for running `sphinx-apidoc`_ on each build.

Overview
--------

*sphinx-apidoc* is a tool for automatic generation of Sphinx sources that,
using the `autodoc`_ extension, document a whole package in the style of other
automatic API documentation tools. *sphinx-apidoc* does not actually build
documentation - rather it simply generates it. As a result, it must be run
before *sphinx-build*. This generally results in ``tox.ini`` files like the
following:

.. code-block:: ini

    [testenv:docs]
    commands =
      sphinx-apidoc -o doc/api my_code my_code/tests
      sphinx-build -W -b html doc doc/_build/html

This extension eliminates the need to keep that configuration outside Sphinx.
Instead, this functionality can be enabled and configured from your
documentation's ``conf.py`` file, like so:

.. code-block:: python

    extensions = [
        'sphinxcontrib.apidoc',
        # ...
    ]
    apidoc_module_dir = '../my_code'
    apidoc_output_dir = 'reference'
    apidoc_excluded_paths = ['tests']

Configuration
-------------

The *apidoc* extension uses the following configuration values:

``apidoc_module_dir``
   The path to the module to document. This must be a path to a Python package.
   This path can be a path relative to the documentation source directory or an
   absolute path.

   **Required**

``apidoc_output_dir``
   The output directory. If it does not exist, it is created. This path is
   relative to the documentation source directory.

   **Optional**, defaults to ``api``.

``apidoc_excluded_paths``
   An optional list of modules to exclude. These should be paths relative to
   ``apidoc_module_dir``. fnmatch-style wildcarding is supported.

   **Optional**, defaults to ``[]``.

Links
-----

- Source: https://github.com/sphinx-contrib/apidoc
- Bugs: https://github.com/sphinx-contrib/apidoc/issues

.. Links

.. _sphinx-apidoc: http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html
.. _autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html

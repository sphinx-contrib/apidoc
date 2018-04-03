====================
sphinxcontrib-apidoc
====================

.. image:: https://travis-ci.org/sphinx-contrib/apidoc.svg?branch=master
    :target: https://travis-ci.org/sphinx-contrib/apidoc

A Sphinx extension for running `sphinx-apidoc`_ on each build.

Overview
--------

*sphinx-apidoc* is a tool for automatic generation of Sphinx sources that,
using the `autodoc <sphinx_autodoc>`_ extension, document a whole package in
the style of other automatic API documentation tools. *sphinx-apidoc* does not
actually build documentation - rather it simply generates it. As a result, it
must be run before *sphinx-build*. This generally results in ``tox.ini`` files
like the following:

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
    apidoc_separate_modules = True

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

``apidoc_separate_modules``
   Put documentation for each module on its own page. Otherwise there will be
   one page per (sub)package.

   **Optional**, defaults to ``False``.

Migration from pbr
------------------

`pbr`_ has historically included a `custom variant <build_sphinx>`_ of the
``build_sphinx`` distutils command. This provides, among other things, the
ability to generate API documentation as part of build process. Clearly this is
not necessary with this extension.

There are two implementations of the API documentation feature in *pbr*:
*autodoc_tree* and *autodoc*. To describe the difference, let's explore how one
would migrate real-world projects using both features.

autodoc_tree
~~~~~~~~~~~~

As *autodoc_tree* is based on *sphinx-apidoc*, migration is easy. Lets take
`python-openstackclient`_ as an example, looking at minimal versions of
``setup.cfg`` and ``doc/source/conf.py``:

.. code-block:: ini

   [build_sphinx]
   all_files = 1
   build-dir = doc/build
   source-dir = doc/source

   [pbr]
   autodoc_tree_index_modules = True
   autodoc_tree_excludes =
     setup.py
     openstackclient/volume/v3
     openstackclient/tests/
     openstackclient/tests/*
   api_doc_dir = contributor/api

.. code-block:: python

   extensions = ['']

Once migrated, this would look like so:

.. code-block:: ini

   [build_sphinx]
   all_files = 1
   build-dir = doc/build
   source-dir = doc/source

.. code-block:: python

   extensions = ['sphinxcontrib.apidoc']

   apidoc_module_dir = '../../openstack'
   apidoc_excluded_paths = [
     'volume',
     'tests'
   ]
   apidoc_output_dir = 'contributor/api'

.. note::

    You could also remove the ``[build_sphinx]`` section from ``setup.cfg`` if
    you wished to build documentation with ``sphinx-build`` directly instead.

There are a couple of changes here:

- Replace ``autodoc_tree_index_modules`` with ``apidoc_module_dir``

  ``autodoc_tree_index_modules`` is boolean option indicating whether to enable
  generation; however, when enabled, docs are always generated for any module
  in the top level directory (where ``setup.cfg`` is located). By comparison
  the extension is already enabled by adding it the ``extension`` attribute of
  ``conf.py``; however, it is necessary to state the directory that you wish to
  document. As a result, it is necessary to remove
  ``autodoc_tree_index_modules`` from ``setup.cfg`` and define
  ``apidoc_module_dir`` in ``conf.py``.

- Replace ``autodoc_tree_excludes`` with ``apidoc_excluded_paths``

  Like ``apidoc_excluded_paths``, ``autodoc_tree_excludes`` is a list of
  fnmatch-style paths describing files and directories to exclude relative to
  the source directory. This means it's a like-for-like replacement so you can
  simply move the option to ``conf.py``, update the paths (assuming
  ``apidoc_module_dir`` is configured to anything except ``.``), and rename it.

- Replace ``api_doc_dir`` with ``apidoc_output_dir``

  As above, ``api_doc_dir`` functions exactly as ``apidoc_output_dir`` does.
  Simply move the option to ``conf.py`` and rename it.

Once done, your output should work exactly as before.

autodoc
~~~~~~~

*autodoc* is not based on *sphinx-apidoc*. Fortunately it is possible to
generate something very similar (although not identical!). Let's take
`oslo.privsep`_ as an example, once again looking at minimal versions of
``setup.cfg`` and ``doc/source/conf.py``:

.. code-block:: ini

   [build_sphinx]
   all_files = 1
   build-dir = doc/build
   source-dir = doc/source

   [pbr]
   autodoc_index_modules = True
   api_doc_dir = reference/api
   autodoc_exclude_modules =
     oslo_privsep.tests.*
     oslo_privsep._*

.. code-block:: python

   extensions = ['']

Once migrated, this would look like so:

.. code-block:: ini

   [build_sphinx]
   all_files = 1
   build-dir = doc/build
   source-dir = doc/source

.. code-block:: python

   extensions = ['sphinxcontrib.apidoc']

   apidoc_module_dir = '../../oslo_privsep'
   apidoc_excluded_paths = ['tests', '_*']
   apidoc_output_dir = 'reference/api'
   apidoc_separate_modules = True

Most of the changes necessary are the same as `autodoc_tree`_, with some
exceptions.

- Replace ``autodoc_index_modules`` with ``apidoc_module_dir``

  Same as the step required for *autodoc_tree*, but you're removing
  ``autodoc_index_modules`` instead of ``autodoc_tree_index_modules``.

- Replace ``autodoc_tree_excludes`` with ``apidoc_excluded_paths``

  ``autodoc_exclude_modules`` differs from ``apidoc_excluded_paths`` and
  ``autodoc_tree_excludes`` in that it's a list of fnmatch-style **module
  paths** - not file paths. As a result, you must switch from ``x.y`` format to
  ``x/y``. These paths should be relative to ``apidoc_module_dir``, not
  ``setup.cfg`` as before.

- Replace ``api_doc_dir`` with ``apidoc_output_dir``

  Same as the step required for *autodoc_tree*.

- Configure ``apidoc_separate_modules=True``

  By default, *sphinx-apidoc* generates a document per package while *autodoc*
  generates a document per (sub)module. By setting this attribute to ``True``,
  we ensure the latter behavior is used.

Links
-----

- Source: https://github.com/sphinx-contrib/apidoc
- Bugs: https://github.com/sphinx-contrib/apidoc/issues

.. Links

.. _sphinx-apidoc: http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html
.. _sphinx_autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
.. _pbr: https://docs.openstack.org/pbr/
.. _build_sphinx: https://docs.openstack.org/pbr/latest/user/using.html#build-sphinx
.. _python-openstackclient: https://github.com/openstack/python-openstackclient/tree/3.15.0
.. _oslo.privsep: https://github.com/openstack/oslo.privsep/tree/1.28.0

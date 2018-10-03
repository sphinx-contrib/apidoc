====================
sphinxcontrib-apidoc
====================

.. image:: https://travis-ci.org/sphinx-contrib/apidoc.svg?branch=master
    :target: https://travis-ci.org/sphinx-contrib/apidoc

A Sphinx extension for running `sphinx-apidoc`_ on each build.

Overview
--------

*sphinx-apidoc* is a tool for automatic generation of Sphinx sources that,
using the `autodoc <sphinx_autodoc>`_ extension, documents a whole package in
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

``apidoc_toc_file``
   Filename for a table of contents file. Defaults to ``modules``. If set to
   ``False``, *apidoc* will not create a table of contents file.

   **Optional**, defaults to ``modules``.

``apidoc_module_first``
   When set to ``True``, put module documentation before submodule
   documentation.

   **Optional**, defaults to ``False``.

``apidoc_extra_args``
   Extra arguments which will be passed to ``sphinx-apidoc``. These are placed
   after flags and before the module name.

   **Optional**, defaults to ``[]``.

Migration from pbr
------------------

`pbr`_ has historically included a custom variant of the `build_sphinx`_
distutils command. This provides, among other things, the ability to generate
API documentation as part of build process. Clearly this is not necessary with
this extension.

There are two implementations of the API documentation feature in *pbr*:
*autodoc_tree* and *autodoc*. To describe the difference, let's explore how one
would migrate real-world projects using both features. Your project might use
one or both: *autodoc_tree* is enabled using the ``autodoc_tree_index_modules``
setting while *autodoc* is enabled using the ``autodoc_index_modules``
setting, both found in the ``[pbr]`` section of ``setup.cfg``.

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

There are a couple of changes here:

#. Configure ``apidoc_module_dir`` in ``conf.py``

   With the *autodoc_tree* feature, API documentation is always generated for
   the directory in which ``setup.cfg`` exists, which is typically the
   top-level directory. With this extension, you must explicitly state which
   directory you wish to build documentation for using the
   ``apidoc_module_dir`` setting. You should configure this to point to your
   actual package rather than the top level directory as this means you don't
   need to worry about skipping unrelated files like ``setup.py``.

#. Configure ``apidoc_excluded_paths`` in ``conf.py``

   The ``apidoc_excluded_paths`` setting in ``conf.py`` works exactly like the
   ``[pbr] autodoc_tree_excludes`` setting in ``setup.cfg``; namely, it's a
   list of fnmatch-style paths describing files and directories to exclude
   relative to the source directory. This means you can use the values from the
   ``[pbr] autodoc_tree_excludes`` setting, though you may need to update
   these if you configured ``apidoc_module_dir`` to point to something other
   than the top-level directory.

#. Configure ``apidoc_output_dir`` in ``conf.py``

   The ``apidoc_output_dir`` setting in ``conf.py`` works exactly like the
   ``[pbr] api_doc_dir`` setting in ``setup.cfg``; namely, it's a path relative
   to the documentation source directory to which all API documentation should
   be written. You can just copy the value from the ``[pbr] api_doc_dir``
   setting.

#. Remove settings from ``setup.cfg``

   Remove the following settings from the ``[pbr]`` section of the
   ``setup.cfg`` file:

   - ``autodoc_tree_index_modules``
   - ``autodoc_tree_excludes``
   - ``api_doc_dir``

   You may also wish to remove the entirety of the ``[build_sphinx]`` section,
   should you wish to build docs using ``sphinx-build`` instead.

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

#. Configure ``apidoc_module_dir`` in ``conf.py``

   With the *autodoc* feature, API documentation is always generated for
   the directory in which ``setup.cfg`` exists, which is typically the
   top-level directory. With this extension, you must explicitly state which
   directory you wish to build documentation for using the
   ``apidoc_module_dir`` setting. You should configure this to point to your
   actual package rather than the top level directory as this means you don't
   need to worry about skipping unrelated files like ``setup.py``.

#. Configure ``apidoc_excluded_paths`` in ``conf.py``

   The  ``apidoc_excluded_paths`` setting in ``conf.py`` differs from the
   ``[pbr] autodoc_exclude_modules`` setting in ``setup.cfg`` in that the
   former is a list of fnmatch-style **file paths**, while the latter is a list
   of fnmatch-style **module paths**. As a result, you can reuse most of the
   values from the ``[pbr] autodoc_exclude_modules`` setting but you must
   switch from ``x.y`` format to ``x/y``. You may also need to update these
   paths if you configured ``apidoc_module_dir`` to point to something other
   than the top-level directory.

#. Configure ``apidoc_output_dir`` in ``conf.py``

   The ``apidoc_output_dir`` setting in ``conf.py`` works exactly like the
   ``[pbr] api_doc_dir`` setting in ``setup.cfg``; namely, it's a path relative
   to the documentation source directory to which all API documentation should
   be written. You can just copy the value from the ``[pbr] api_doc_dir``
   setting.

#. Configure ``apidoc_separate_modules=True`` in ``conf.py``

   By default, *sphinx-apidoc* generates a document per package while *autodoc*
   generates a document per (sub)module. By setting this attribute to ``True``,
   we ensure the latter behavior is used.

#. Replace references to ``autoindex.rst`` with ``modules.rst``

   The *autodoc* feature generates a list of modules in a file called
   ``autoindex.rst`` located in the output directory. By comparison,
   *sphinx-apidoc* and this extension call this file ``modules.rst``. You must
   update all references to ``autoindex.rst`` with ``modules.rst`` instead. You
   may also wish to configure the ``depth`` option of any ``toctree``\s that
   include this document as ``modules.rst`` is nested.

#. Remove settings from ``setup.cfg``

   Remove the following settings from the ``[pbr]`` section of the
   ``setup.cfg`` file:

   - ``autodoc_index_modules``
   - ``autodoc_exclude_modules``
   - ``api_doc_dir``

   You may also wish to remove the entirety of the ``[build_sphinx]`` section,
   should you wish to build docs using ``sphinx-build`` instead.

Once done, your output should look similar to previously. The main change will
be in the aforementioned ``modules.rst``, which uses a nested layout compared
to the flat layout of the ``autoindex.rst`` file.

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

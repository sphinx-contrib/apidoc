# -*- coding: utf-8 -*-
"""
    test_apidoc
    ~~~~~~~~~~~

    Test the sphinxcontrib.apidoc module.

    :copyright: Copyright 2018-present by Stephen Finucane <stephen@that.guru>
    :license: BSD, see LICENSE for details.
"""

import pytest
import sphinx
from sphinx.util import logging


def is_dir(path):
    if sphinx.version_info >= (7, 2, 0):
        return path.is_dir()
    else:
        return path.isdir()


@pytest.mark.sphinx('html', testroot='basics')
def test_basics(app, status, warning):
    logging.setup(app, status, warning)
    app.builder.build_all()

    assert is_dir(app.srcdir / 'api')
    assert (app.srcdir / 'api' / 'modules.rst').exists()
    assert (app.srcdir / 'api' / 'apidoc_dummy_module.rst').exists()
    assert not (app.srcdir / 'api' / 'conf.rst').exists()

    assert is_dir(app.outdir / 'api')
    assert (app.outdir / 'api' / 'modules.html').exists()
    assert (app.outdir / 'api' / 'apidoc_dummy_module.html').exists()
    assert not (app.outdir / 'api' / 'conf.html').exists()

    assert not warning.getvalue()


@pytest.mark.sphinx('html', testroot='advanced')
def test_advanced(app, status, warning):
    if sphinx.version_info < (1, 8, 0):
        pytest.xfail('This should fail on older Sphinx versions')

    logging.setup(app, status, warning)
    app.builder.build_all()

    assert is_dir(app.srcdir / 'api')
    assert (app.srcdir / 'api' / 'custom.rst').exists()
    for module in [
        'apidoc_dummy_module.rst',
        'apidoc_dummy_package.apidoc_dummy_submodule_a.rst',
        'apidoc_dummy_package.apidoc_dummy_submodule_b.rst',
        'apidoc_dummy_package._apidoc_private_dummy_submodule.rst',
    ]:
        assert (app.srcdir / 'api' / module).exists()
    assert (app.srcdir / 'api' / 'apidoc_dummy_package.rst').exists()
    assert not (app.srcdir / 'api' / 'conf.rst').exists()

    with open(app.srcdir / 'api' / 'apidoc_dummy_package.rst') as fh:
        package_doc = [x.strip() for x in fh.readlines()]

    # The 'Module contents' header isn't present if '--module-first' used
    assert 'Module contents' not in package_doc

    assert is_dir(app.outdir / 'api')
    assert (app.outdir / 'api' / 'custom.html').exists()
    for module in [
        'apidoc_dummy_module.html',
        'apidoc_dummy_package.apidoc_dummy_submodule_a.html',
        'apidoc_dummy_package.apidoc_dummy_submodule_b.html',
        'apidoc_dummy_package._apidoc_private_dummy_submodule.html',
    ]:
        assert (app.outdir / 'api' / module).exists()
    assert (app.outdir / 'api' / 'apidoc_dummy_package.html').exists()
    assert not (app.outdir / 'api' / 'conf.html').exists()

    assert not warning.getvalue()


@pytest.mark.sphinx('html', testroot='advanced-negative')
def test_advanced_negative(app, status, warning):
    """The "test_advanced" test but with boolean options toggled."""
    logging.setup(app, status, warning)
    app.builder.build_all()

    assert is_dir(app.srcdir / 'api')
    for module in [
        'apidoc_dummy_module.rst',
    ]:
        assert (app.srcdir / 'api' / module).exists()
    assert (app.srcdir / 'api' / 'apidoc_dummy_package.rst').exists()
    assert not (app.srcdir / 'api' / 'custom.rst').exists()
    assert not (app.srcdir / 'api' / 'conf.rst').exists()

    with open(app.srcdir / 'api' / 'apidoc_dummy_package.rst') as fh:
        package_doc = [x.strip() for x in fh.readlines()]

    # The 'Module contents' header is present if '--module-first' isn't used
    assert 'Module contents' in package_doc

    assert is_dir(app.outdir / 'api')
    for module in [
        'apidoc_dummy_module.html',
    ]:
        assert (app.outdir / 'api' / module).exists()
    assert (app.outdir / 'api' / 'apidoc_dummy_package.html').exists()
    assert not (app.outdir / 'api' / 'custom.html').exists()
    assert not (app.outdir / 'api' / 'conf.html').exists()

    assert not warning.getvalue()


@pytest.mark.sphinx('html', testroot='missing-configuration')
def test_missing_configuration(app, status, warning):
    logging.setup(app, status, warning)
    app.builder.build_all()
    assert not (app.outdir / 'api').exists()
    assert "No 'apidoc_module_dir' specified" in warning.getvalue()


@pytest.mark.sphinx('html', testroot='invalid-directory')
def test_invalid_directory(app, status, warning):
    logging.setup(app, status, warning)
    app.builder.build_all()
    assert not (app.outdir / 'api').exists()
    assert "The path defined in 'apidoc_module_dir'" in warning.getvalue()

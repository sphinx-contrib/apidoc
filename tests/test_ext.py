# -*- coding: utf-8 -*-
"""
    test_apidoc
    ~~~~~~~~~~~

    Test the sphinxcontrib.apidoc module.

    :copyright: Copyright 2018 by Stephen Finucane <stephen@that.guru>.
    :license: BSD, see LICENSE for details.
"""

import pytest
from sphinx.util import logging


@pytest.mark.sphinx('html', testroot='basics')
def test_basics(app, status, warning):
    logging.setup(app, status, warning)
    app.builder.build_all()
    assert (app.outdir / 'api').isdir()
    assert (app.outdir / 'api' / 'modules.html').exists()
    assert (app.outdir / 'api' / 'apidoc_dummy_module.html').exists()
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

# -*- coding: utf-8 -*-
"""
    test_apidoc
    ~~~~~~~~~~~

    Test the sphinxcontrib.apidoc module.

    :copyright: Copyright 2018 by Stephen Finucane <stephen@that.guru>.
    :license: BSD, see LICENSE for details.
"""

import pytest


@pytest.mark.sphinx('html', testroot='apidoc')
def test_apidoc_extension(app, status, warning):
    app.builder.build_all()
    assert (app.outdir / 'api').isdir()
    assert (app.outdir / 'api' / 'modules.html').exists()
    assert (app.outdir / 'api' / 'apidoc_dummy_module.html').exists()
    assert not (app.outdir / 'api' / 'conf.html').exists()

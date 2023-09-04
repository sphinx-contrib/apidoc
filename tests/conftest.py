"""
    pytest config for sphinxcontrib/apidoc/tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2018-present by Stephen Finucane <stephen@that.guru>
    :license: BSD, see LICENSE for details.
"""

import os
import tempfile

import pytest
import sphinx

pytest_plugins = 'sphinx.testing.fixtures'

collect_ignore = ['roots']


@pytest.fixture(scope='session')
def sphinx_test_tempdir():
    if sphinx.version_info >= (7, 2, 0):
        from pathlib import Path

        return Path(
            os.environ.get('SPHINX_TEST_TEMPDIR', tempfile.mkdtemp(prefix='apidoc-'))
        ).resolve()
    else:
        from sphinx.testing.path import path

        return path(
            os.environ.get('SPHINX_TEST_TEMPDIR', tempfile.mkdtemp(prefix='apidoc-'))
        ).abspath()


@pytest.fixture(scope='session')
def rootdir():
    if sphinx.version_info >= (7, 2, 0):
        from pathlib import Path

        return Path(os.path.dirname(__file__) or '.').resolve() / 'roots'
    else:
        from sphinx.testing.path import path

        return path(os.path.dirname(__file__) or '.').abspath() / 'roots'

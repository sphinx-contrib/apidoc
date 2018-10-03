"""
    pytest config for sphinxcontrib/apidoc/tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by Stephen Finucane <stephen@that.guru>
    :license: BSD, see LICENSE for details.
"""

import os
import tempfile

import pytest
from sphinx.testing.path import path

pytest_plugins = 'sphinx.testing.fixtures'

collect_ignore = ['roots']


@pytest.fixture(scope='session')
def sphinx_test_tempdir():
    return path(
        os.environ.get('SPHINX_TEST_TEMPDIR',
                       tempfile.mkdtemp(prefix='apidoc-'))).abspath()


@pytest.fixture(scope='session')
def rootdir():
    return path(os.path.dirname(__file__) or '.').abspath() / 'roots'

"""
    pytest config for sphinxcontrib/apidoc/tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by Stephen Finucane <stephen@that.guru>
    :license: BSD, see LICENSE for details.
"""

import os
import tempfile

import pytest
from pathlib import Path

pytest_plugins = 'sphinx.testing.fixtures'

collect_ignore = ['roots']


@pytest.fixture(scope='session')
def sphinx_test_tempdir():
    return Path(
        os.environ.get('SPHINX_TEST_TEMPDIR',
                       tempfile.mkdtemp(prefix='apidoc-'))).resolve()

@pytest.fixture(scope='session')
def rootdir():
    return Path(os.path.dirname(__file__) or '.').resolve() / 'roots'

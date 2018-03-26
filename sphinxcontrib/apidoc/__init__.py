"""
    sphinxcontrib.apidoc
    ~~~~~~~~~~~~~~~~~~~~

    A Sphinx extension for running 'sphinx-apidoc' on each build.

    :copyright: Copyright 2018 by Stephen Finucane <stephen@that.guru>
    :license: BSD, see LICENSE for details.
"""

import pbr.version


__version__ = pbr.version.VersionInfo(
    'apidoc').version_string()

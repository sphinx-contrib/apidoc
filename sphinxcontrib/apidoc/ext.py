"""
    sphinxcontrib.apidoc.ext
    ~~~~~~~~~~~~~~~~~~~~~~~~

    A Sphinx extension for running 'sphinx-apidoc' on each build.

    :copyright: Copyright 2018 by Stephen Finucane <stephen@that.guru>
    :license: BSD, see LICENSE for details.
"""

from os import path

from sphinx.util import logging

try:
    from sphinx.ext import apidoc  # Sphinx >= 1.7
except ImportError:
    from sphinx import apidoc  # Sphinx < 1.7

if False:
    # For type annotation
    from sphinx.application import Sphinx  # noqa

logger = logging.getLogger(__name__)


def builder_inited(app):
    # type: (Sphinx) -> None
    module_dir = app.config.apidoc_module_dir
    output_dir = path.join(app.srcdir, app.config.apidoc_output_dir)
    excludes = app.config.apidoc_excluded_paths

    if not module_dir:
        logger.warning("No 'apidoc_module_dir' specified; skipping API doc "
                       "generation")
        return

    # if the path is relative, make it relative to the 'conf.py' directory
    if not path.isabs(module_dir):
        module_dir = path.abspath(path.join(app.srcdir, module_dir))

    if not path.exists(module_dir):
        logger.warning("The path defined in 'apidoc_module_dir' does not "
                       "exist; skipping API doc generation; %s", module_dir)
        return

    excludes = [path.abspath(path.join(module_dir, exc)) for exc in excludes]

    # refactor this module so that we can call 'recurse_tree' like a sane
    # person - at present there is way too much passing around of the
    # 'optparse.Value' instance returned by 'optparse.parse_args'
    cmd = ['--force', '-o', output_dir, module_dir]
    if excludes:
        cmd += excludes

    apidoc.main(cmd)

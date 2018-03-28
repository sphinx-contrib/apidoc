# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath('./'))

extensions = ['sphinxcontrib.apidoc']
master_doc = 'index'

apidoc_module_dir = '.'
apidoc_excluded_paths = ['conf.py']

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax',
    'nbsphinx'
]


exclude_patterns = ['_build', '**.ipynb_checkpoints']

nbsphinx_allow_errors = True
nbsphinx_timeout = 360


if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True
    spelling_lang = 'en_GB'

source_suffix = '.rst'
master_doc = 'index'
project = 'oemof.datapackage'
year = '2025'
author = 'Stephan Günther, Jann Launer, Julian Endres, Hendrik Huyskens'
copyright = '{0}, {1}'.format(year, author)
version = release = '0.0.6dev'

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('https://github.com/oemof/oemof-datapackage/issues/%s', '#'),
    'pr': ('https://github.com/oemof/oemof-datapackage/pull/%s', 'PR #'),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

html_theme = 'sphinx_rtd_theme'

html_theme_options = { "collapse_navigation": False, }

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False

# Options for Sphinx autodoc
autodoc_mock_imports = [
    "tsam",
    "shapely",
    "pyproj",
    "geojson",
    "scipy",
    "shapefile",
]

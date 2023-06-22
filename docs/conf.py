# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

from oemof.tabular.facades import TYPEMAP

sys.path.append("code")
from get_facade_attributes import get_facade_attrs, write_table_rst

facade_attrs = get_facade_attrs(TYPEMAP)
for facade, attrs in facade_attrs.items():
    attrs.to_csv(os.path.join("facade_attributes", facade + ".csv"))
write_table_rst("facade_attributes", "facades.rst")

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
    spelling_lang = 'en_US'

source_suffix = '.rst'
master_doc = 'index'
project = 'oemof.tabular'
year = '2018'
author = 'Stephan Günther'
copyright = '{0}, {1}'.format(year, author)
version = release = '0.0.4dev'

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('https://github.com/oemof/oemof-tabular/issues/%s', '#'),
    'pr': ('https://github.com/oemof/oemof-tabular/pull/%s', 'PR #'),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only set the theme if we're building docs locally
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

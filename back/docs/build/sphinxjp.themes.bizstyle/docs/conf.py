# -*- coding: utf-8 -*-
#
# -- General configuration -------------------------------------

source_suffix = '.rst'
master_doc = 'index'

project = u'Sphinx theme for Business style'
copyright = u'2011, Sphinx-users.jp'

version = '0.1.5'

# -- Options for HTML output -----------------------------------

extensions = ['sphinxjp.themecore']
html_theme = 'bizstyle'

html_theme_options = {
    'rightsidebar': False,
}


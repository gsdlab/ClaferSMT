# -*- coding: utf-8 -*-
#
# -- General configuration -----------------------------------------------------

source_suffix = '.rst'
master_doc = 'index'

project = u'sphinx theme for dotted style'
copyright = u'2011, Sphinx-users.jp'

version = '0.1.1'

# -- Options for HTML output ---------------------------------------------------

extensions = ['sphinxjp.themecore']
html_theme = 'dotted'

# -- HTML theme options for `dotted` style -------------------------------------

html_theme_options = {
    'slidetoc': True,
    'enablesidebar': True,
    'rightsidebar': True,
}

# SPDX-License-Identifier: BSD-3-Clause
from datetime      import date
from pathlib       import Path

from usb_construct import __version__ as usb_construct_version

ROOT_DIR = (Path(__file__).parent).parent

project   = 'usb-construct'
version   = usb_construct_version
release   = version.split('+')[0]
copyright = f'{date.today().year} Shrine Maiden Heavy Industries, et. al.'
language  = 'en'

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.extlinks',
	'sphinx.ext.githubpages',
	'sphinx.ext.intersphinx',
	'sphinx.ext.napoleon',
	'sphinx.ext.todo',
	'myst_parser',
	'sphinx_copybutton',
]

source_suffix = {
	'.rst': 'restructuredtext',
	'.md': 'markdown',
}

extlinks = {
	'issue': ('https://github.com/shrine-maiden-heavy-industries/usb-construct/issues/%s', 'usb-construct/%s'),
	'pypi':  ('https://pypi.org/project/%s/', '%s'),
}

pygments_style              = 'default'
pygments_dark_style         = 'monokai'
autodoc_member_order        = 'bysource'
autodoc_docstring_signature = False
todo_include_todos          = True

intersphinx_mapping = {
	'python'   : ('https://docs.python.org/3', None),
	'construct': ('https://construct.readthedocs.io/en/latest', None),
}

napoleon_google_docstring              = False
napoleon_numpy_docstring               = True
napoleon_use_ivar                      = True
napoleon_use_admonition_for_notes      = True
napoleon_use_admonition_for_examples   = True
napoleon_use_admonition_for_references = True
napoleon_custom_sections  = [
	('Attributes', 'params_style'),
]

myst_heading_anchors = 3

templates_path = [
	'_templates',
]


html_baseurl     = 'https://usb-construct.shmdn.link/'
html_theme       = 'furo'
html_copy_source = False

html_theme_options = {

}

html_static_path = [
	'_static'
]

html_css_files = [
	'css/styles.css'
]

autosectionlabel_prefix_document = True

linkcheck_retries = 2
linkcheck_workers = 1 # At the cost of speed try to prevent rate-limiting
linkcheck_ignore  = []

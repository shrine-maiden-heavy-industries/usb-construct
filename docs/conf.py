# SPDX-License-Identifier: BSD-3-Clause
import os, sys, datetime
from pathlib import Path
sys.path.insert(0, os.path.abspath('.'))

from usb_construct import __version__ as usb_construct_version

ROOT_DIR = (Path(__file__).parent).parent

def doc_version():
	try:
		from setuptools_scm.git import parse as parse_git
	except ImportError:
		return ''

	git = parse_git(str(ROOT_DIR.resolve()))
	if not git:
		return ''
	elif git.exact:
		return git.format_with('v{tag}')
	else:
		return 'latest'

project   = 'usb-construct'
version   = usb_construct_version
release   = version.split('+')[0]
copyright = f'{datetime.date.today().year} Shrine Maiden Heavy Industries, et. al.'
language  = 'en'
docver    = doc_version()

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.doctest',
	'sphinx.ext.githubpages',
	'sphinx.ext.intersphinx',
	'sphinx.ext.napoleon',
	'sphinx.ext.todo',
	'myst_parser',
	'sphinx_rtd_theme',
]

with (ROOT_DIR / '.gitignore').open('r') as f:
	exclude_patterns = [line.strip() for line in f.readlines()]


source_suffix = {
	'.rst': 'restructuredtext',
	'.md': 'markdown',
}

pygments_style         = 'monokai'
autodoc_member_order   = 'bysource'
graphviz_output_format = 'svg'
todo_include_todos     = True

intersphinx_mapping = {
	'python'   : ('https://docs.python.org/3', None),
	'construct': ('https://construct.readthedocs.io/en/latest', None),
}

napoleon_google_docstring = False
napoleon_numpy_docstring  = True
napoleon_use_ivar         = True

myst_heading_anchors = 3

templates_path = [
	'_templates',
]

html_context = {
	'display_lower_left': False,
	'current_language'  : language,
	'current_version'   : docver,
	'version'           : docver,
	'display_github'    : True,
	'github_user'       : 'shrine-maiden-heavy-industries',
	'github_repo'       : 'usb-construct',
	'github_version'    : 'main/docs/',
	'versions'          : [
		('latest', '/latest')
	]
}

html_baseurl     = 'https://usb-construct.shmdn.link/'
html_theme       = 'sphinx_rtd_theme'
html_copy_source = False

html_theme_options = {
	'collapse_navigation' : False,
	'style_external_links': True,
}

html_static_path = [
	'_static'
]

html_css_files = [
	'css/styles.css'
]
html_style = 'css/styles.css'
autosectionlabel_prefix_document = True
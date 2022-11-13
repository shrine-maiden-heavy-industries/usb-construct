#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause

from setuptools import setup, find_packages
from pathlib    import Path

REPO_ROOT   = Path(__file__).parent
README_FILE = (REPO_ROOT / 'README.md')

def vcs_ver():
	def scheme(version):
		if version.tag and not version.distance:
			return version.format_with('')
		else:
			return version.format_choice('+{node}', '+{node}.dirty')
	return {
		'relative_to': __file__,
		'version_scheme': 'guess-next-dev',
		'local_scheme': scheme
	}

setup(
	name             = 'usb-construct',
	use_scm_version  = vcs_ver(),
	license          = 'BSD-3-Clause',
	url              = 'https://github.com/shrine-maiden-heavy-industries/usb-construct',
	author           = 'Katherine J. Temkin',
	author_email     = 'k@ktemkin.com',
	maintainer       = ', '.join([
		'Aki Van Ness',
		'Rachel Mant',
	]),
	maintainer_email = ', '.join([
		'aki@lethalbit.net',
		'git@dragonmux.network',
	]),
	description      = 'python library providing utilities, data structures, constants, parsers, and tools for working with USB data',

	long_description = README_FILE.read_text(),
	long_description_content_type = 'text/markdown',


	setup_requires   = [
		'wheel',
		'setuptools',
		'setuptools_scm',
	],
	packages         = find_packages(
		where = '.'
	),
	python_requires  = '~=3.9',
	install_requires = [
		'construct',
	],
	extras_require = {
		'dev': [
			'nox'
		],
	},
	classifiers      = [
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Environment :: Plugins',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: BSD License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
		'Programming Language :: Python :: 3.11',



		'Topic :: Scientific/Engineering',
		'Topic :: Security',
		'Topic :: Software Development :: Libraries',
		'Topic :: System :: Hardware :: Universal Serial Bus (USB)',

	],
	project_urls      = {
		'Documentation': 'https://github.com/shrine-maiden-heavy-industries/usb-construct',
		'Source Code': 'https://github.com/shrine-maiden-heavy-industries/usb-construct',
		'Bug Tracker': 'https://github.com/shrine-maiden-heavy-industries/usb-construct/issues',
	},
)

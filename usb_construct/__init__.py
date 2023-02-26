# SPDX-License-Identifier: BSD-3-Clause
try:
	from importlib import metadata
	__version__ = metadata.version(__package__)
except ImportError:
	__version__ = 'unknown' # :nocov:

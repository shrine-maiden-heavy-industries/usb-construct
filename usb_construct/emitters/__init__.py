# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
''' USB-related emitters. '''

from .construct_interop    import emitter_for_format, ConstructEmitter
from .descriptors.standard import (
	DeviceDescriptorCollection, SuperSpeedDeviceDescriptorCollection
)

__all__ = (
	'emitter_for_format',
	'ConstructEmitter',
	'DeviceDescriptorCollection',
	'SuperSpeedDeviceDescriptorCollection',
)

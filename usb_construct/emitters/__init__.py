# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
''' USB-related emitters. '''

from .construct_interop    import ConstructEmitter, emitter_for_format
from .descriptors.standard import DeviceDescriptorCollection, SuperSpeedDeviceDescriptorCollection

__all__ = (
	'ConstructEmitter',
	'DeviceDescriptorCollection',
	'emitter_for_format',
	'SuperSpeedDeviceDescriptorCollection',
)

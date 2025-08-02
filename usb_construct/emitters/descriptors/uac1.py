# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
''' Convenience emitters for USB Audio Class 1 descriptors. '''

from ...types.descriptors.uac1 import AudioControlInterruptEndpointDescriptor
from ..                        import emitter_for_format

AudioControlInterruptEndpointDescriptorEmitter = emitter_for_format(
	AudioControlInterruptEndpointDescriptor
)

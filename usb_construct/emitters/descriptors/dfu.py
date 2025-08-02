# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
''' Convenience emitters for simple, DFU descriptors. '''

from ...types.descriptors.dfu import FunctionalDescriptor
from ..                       import emitter_for_format

# Create our basic emitters...
FunctionalDescriptorEmitter = emitter_for_format(FunctionalDescriptor)

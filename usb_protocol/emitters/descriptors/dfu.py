#
# This file is part of usb_protocol.
#
""" Convenience emitters for simple, DFU descriptors. """

from ..           import emitter_for_format

from ...types.descriptors.dfu import *


# Create our basic emitters...
FunctionalDescriptorEmitter         = emitter_for_format(FunctionalDescriptor)

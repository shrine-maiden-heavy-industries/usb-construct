# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
''' Convenience emitters for CDC descriptors. '''

from .. import emitter_for_format
from ...types.descriptors.cdc import \
	HeaderDescriptor, UnionFunctionalDescriptor, ACMFunctionalDescriptor, \
	CallManagementFunctionalDescriptor

# Create our emitters.
HeaderDescriptorEmitter                   = emitter_for_format(HeaderDescriptor)
UnionFunctionalDescriptorEmitter          = emitter_for_format(UnionFunctionalDescriptor)
ACMFunctionalDescriptorEmitter            = emitter_for_format(ACMFunctionalDescriptor)
CallManagementFunctionalDescriptorEmitter = emitter_for_format(CallManagementFunctionalDescriptor)

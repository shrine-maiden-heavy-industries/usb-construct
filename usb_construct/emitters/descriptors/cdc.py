# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
''' Convenience emitters for CDC descriptors. '''

from ...types.descriptors.cdc import (
	ACMFunctionalDescriptor, CallManagementFunctionalDescriptor, HeaderDescriptor,
	UnionFunctionalDescriptor
)
from ..                        import emitter_for_format

# Create our emitters.
HeaderDescriptorEmitter                   = emitter_for_format(HeaderDescriptor)
UnionFunctionalDescriptorEmitter          = emitter_for_format(UnionFunctionalDescriptor)
ACMFunctionalDescriptorEmitter            = emitter_for_format(ACMFunctionalDescriptor)
CallManagementFunctionalDescriptorEmitter = emitter_for_format(
	CallManagementFunctionalDescriptor
)

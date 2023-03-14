# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#

from ...emitters.construct_interop    import ConstructEmitter
from ...emitters.descriptors.dfu      import FunctionalDescriptorEmitter
from ...emitters.descriptors.standard import InterfaceDescriptorEmitter
from ..manager                        import DescriptorContextManager


class FunctionalDescriptor(DescriptorContextManager):
	ParentDescriptor = InterfaceDescriptorEmitter

	def DescriptorEmitter(self) -> ConstructEmitter:
		return FunctionalDescriptorEmitter()

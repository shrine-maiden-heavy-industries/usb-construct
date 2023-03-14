# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#

from typing                       import Optional, Callable, Union
from types                        import TracebackType

from ..emitters.descriptor        import ComplexDescriptorEmitter
from ..emitters.construct_interop import ConstructEmitter


class DescriptorContextManager:
	ParentDescriptor = ComplexDescriptorEmitter
	DescriptorEmitter: Optional[Union[type[Callable[[], ConstructEmitter]], type[ComplexDescriptorEmitter]]] = None

	def __init__(self, parentDesc: ParentDescriptor) -> None:
		if self.DescriptorEmitter is None:
			raise TypeError('DescriptorEmitter must not be None')

		self._parent = parentDesc
		self._descriptor = self.DescriptorEmitter()

	def __enter__(self) -> ConstructEmitter:
		return self._descriptor

	def __exit__(
		self, exc_type: Optional[type[BaseException]], exc_value: BaseException,
		traceback: Optional[TracebackType]
	) -> None:
		# If an exception was raised, fast exit
		if not (exc_type is None and exc_value is None and traceback is None):
			return

		self._parent.add_subordinate_descriptor(self._descriptor)

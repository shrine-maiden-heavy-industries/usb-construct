# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#

from ...emitters.descriptors.standard import InterfaceAssociationDescriptorEmitter, InterfaceDescriptorEmitter
from ...emitters.descriptors.uac3     import (
	ClassSpecificAudioStreamingInterfaceDescriptorEmitter, ClockSourceDescriptorEmitter,
	ConnectorDescriptorEmitter, HeaderDescriptorEmitter, InputTerminalDescriptorEmitter,
	OutputTerminalDescriptorEmitter, PowerDomainDescriptorEmitter,
)
from ..manager import DescriptorContextManager

class HeaderDescriptor(DescriptorContextManager):
	ParentDescriptor  = InterfaceAssociationDescriptorEmitter
	DescriptorEmitter = HeaderDescriptorEmitter

	def __exit__(self, exc_type, exc_value, traceback):
		# If an exception was raised, fast exit
		if not (exc_type is None and exc_value is None and traceback is None):
			return
		self._parent.add_subordinate_descriptor(self._descriptor)
		for sub in self._descriptor._subordinates:
			self._parent.add_subordinate_descriptor(sub)


class InputTerminalDescriptor(DescriptorContextManager):
	ParentDescriptor = HeaderDescriptorEmitter

	def DescriptorEmitter(self) -> InputTerminalDescriptorEmitter:
		return InputTerminalDescriptorEmitter()


class OutputTerminalDescriptor(DescriptorContextManager):
	ParentDescriptor = HeaderDescriptorEmitter

	def DescriptorEmitter(self) -> OutputTerminalDescriptorEmitter:
		return OutputTerminalDescriptorEmitter()


class ClockSourceDescriptor(DescriptorContextManager):
	ParentDescriptor = HeaderDescriptorEmitter

	def DescriptorEmitter(self) -> ClockSourceDescriptorEmitter:
		return ClockSourceDescriptorEmitter()


class PowerDomainDescriptor(DescriptorContextManager):
	ParentDescriptor = HeaderDescriptorEmitter

	def DescriptorEmitter(self) -> PowerDomainDescriptorEmitter:
		return PowerDomainDescriptorEmitter()


class ClassSpecificAudioStreamingInterfaceDescriptor(DescriptorContextManager):
	ParentDescriptor = InterfaceDescriptorEmitter

	def DescriptorEmitter(self) -> ClassSpecificAudioStreamingInterfaceDescriptorEmitter:
		return ClassSpecificAudioStreamingInterfaceDescriptorEmitter()


class ConnectorDescriptor(DescriptorContextManager):
	ParentDescriptor = HeaderDescriptorEmitter

	def DescriptorEmitter(self) -> ConnectorDescriptorEmitter:
		return ConnectorDescriptorEmitter()

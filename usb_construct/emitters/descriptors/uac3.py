# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
""" Convenience emitters for USB Audio Class 3 descriptors. """

from functools import cached_property

from .. import emitter_for_format
from ..descriptor import ConstructEmitter, ComplexDescriptorEmitter

from ...types.descriptors.uac3 import *

InputTerminalDescriptorEmitter                                           = emitter_for_format(InputTerminalDescriptor)
OutputTerminalDescriptorEmitter                                          = emitter_for_format(OutputTerminalDescriptor)
AudioStreamingInterfaceDescriptorEmitter                                 = emitter_for_format(AudioStreamingInterfaceDescriptor)
ClassSpecificAudioStreamingInterfaceDescriptorEmitter                    = emitter_for_format(ClassSpecificAudioStreamingInterfaceDescriptor)
AudioControlInterruptEndpointDescriptorEmitter                           = emitter_for_format(AudioControlInterruptEndpointDescriptor)
AudioStreamingIsochronousEndpointDescriptorEmitter                       = emitter_for_format(AudioStreamingIsochronousEndpointDescriptor)
AudioStreamingIsochronousFeedbackEndpointDescriptorEmitter               = emitter_for_format(AudioStreamingIsochronousFeedbackEndpointDescriptor)


class HeaderDescriptorEmitter(ComplexDescriptorEmitter):
	def __init__(self):
		super().__init__(self.DESCRIPTOR_FORMAT)

	@cached_property
	def DESCRIPTOR_FORMAT(self):
		from usb_construct.emitters.descriptors.uac3 import HeaderDescriptor
		return HeaderDescriptor

	def add_subordinate_descriptor(self, subordinate):
		""" Adds a subordinate descriptor to the relevant parent descriptor.

		Parameter:
			subordinate -- The subordinate descriptor to add; can be an emitter,
							or a bytes-like object.
		"""
		if hasattr(subordinate, 'emit'):
			subordinate = subordinate.emit()
		else:
			subordinate = bytes(subordinate)
		self._subordinates.append(subordinate)

	def _pre_emit(self):
		subordinate_length = sum(len(sub) for sub in self._subordinates)
		self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()


def ClockSourceDescriptorEmitter():
	return ConstructEmitter(ClockSourceDescriptor)


def PowerDomainDescriptorEmitter():
	return ConstructEmitter(PowerDomainDescriptor)


def ConnectorDescriptorEmitter():
	return ConstructEmitter(ConnectorDescriptor)

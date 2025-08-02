# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
''' Convenience emitters for USB Audio Class 2 descriptors. '''

from ...emitters.descriptor    import ComplexDescriptorEmitter
from ...types.descriptors.uac2 import (
	AudioControlInterruptEndpointDescriptor, AudioStreamingInterfaceDescriptor,
	AudioStreamingIsochronousEndpointDescriptor, AudioStreamingIsochronousFeedbackEndpointDescriptor,
	ClassSpecificAudioControlInterfaceDescriptor, ClassSpecificAudioStreamingInterfaceDescriptor,
	ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptor, ClockSourceDescriptor,
	ExtendedTypeIFormatTypeDescriptor, ExtendedTypeIIFormatTypeDescriptor, ExtendedTypeIIIFormatTypeDescriptor,
	FeatureUnitDescriptor, InputTerminalDescriptor, OutputTerminalDescriptor,
	StandardAudioControlInterfaceDescriptor, TypeIFormatTypeDescriptor, TypeIIFormatTypeDescriptor,
	TypeIIIFormatTypeDescriptor,
)
from ..                        import emitter_for_format

# Create our emitters.
StandardAudioControlInterfaceDescriptorEmitter = emitter_for_format(
	StandardAudioControlInterfaceDescriptor
)

class ClassSpecificAudioControlInterfaceDescriptorEmitter(ComplexDescriptorEmitter):
	DESCRIPTOR_FORMAT = ClassSpecificAudioControlInterfaceDescriptor

	def _pre_emit(self) -> None:
		# Figure out the total length of our descriptor, including subordinates.
		subordinate_length = sum(len(sub) for sub in self._subordinates)
		self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

ClockSourceDescriptorEmitter                                             = emitter_for_format(
	ClockSourceDescriptor
)
InputTerminalDescriptorEmitter                                           = emitter_for_format(
	InputTerminalDescriptor
)
OutputTerminalDescriptorEmitter                                          = emitter_for_format(
	OutputTerminalDescriptor
)
FeatureUnitDescriptorEmitter                                             = emitter_for_format(
	FeatureUnitDescriptor
)
AudioStreamingInterfaceDescriptorEmitter                                 = emitter_for_format(
	AudioStreamingInterfaceDescriptor
)
ClassSpecificAudioStreamingInterfaceDescriptorEmitter                    = emitter_for_format(
	ClassSpecificAudioStreamingInterfaceDescriptor
)
TypeIFormatTypeDescriptorEmitter                                         = emitter_for_format(
	TypeIFormatTypeDescriptor
)
ExtendedTypeIFormatTypeDescriptorEmitter                                 = emitter_for_format(
	ExtendedTypeIFormatTypeDescriptor
)
TypeIIFormatTypeDescriptorEmitter                                        = emitter_for_format(
	TypeIIFormatTypeDescriptor
)
ExtendedTypeIIFormatTypeDescriptorEmitter                                = emitter_for_format(
	ExtendedTypeIIFormatTypeDescriptor
)
TypeIIIFormatTypeDescriptorEmitter                                       = emitter_for_format(
	TypeIIIFormatTypeDescriptor
)
ExtendedTypeIIIFormatTypeDescriptorEmitter                               = emitter_for_format(
	ExtendedTypeIIIFormatTypeDescriptor
)
ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptorEmitter = emitter_for_format(
	ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptor
)
AudioControlInterruptEndpointDescriptorEmitter                           = emitter_for_format(
	AudioControlInterruptEndpointDescriptor
)
AudioStreamingIsochronousEndpointDescriptorEmitter                       = emitter_for_format(
	AudioStreamingIsochronousEndpointDescriptor
)
AudioStreamingIsochronousFeedbackEndpointDescriptorEmitter               = emitter_for_format(
	AudioStreamingIsochronousFeedbackEndpointDescriptor
)

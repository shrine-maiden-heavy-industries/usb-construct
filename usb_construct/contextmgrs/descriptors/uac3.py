# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#

from ..manager import DescriptorContextManager

from ...emitters.descriptors.standard import InterfaceAssociationDescriptorEmitter, InterfaceDescriptorEmitter
from ...emitters.descriptors.uac3 import (
    HeaderDescriptorEmitter, InputTerminalDescriptorEmitter, OutputTerminalDescriptorEmitter,
    ClockSourceDescriptorEmitter, PowerDomainDescriptorEmitter, ConnectorDescriptorEmitter,
    ClassSpecificAudioStreamingInterfaceDescriptorEmitter
)


class HeaderDescriptor(DescriptorContextManager):
    ParentDescriptor = InterfaceAssociationDescriptorEmitter
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
    DescriptorEmitter = lambda self: InputTerminalDescriptorEmitter()


class OutputTerminalDescriptor(DescriptorContextManager):
    ParentDescriptor = HeaderDescriptorEmitter
    DescriptorEmitter = lambda self: OutputTerminalDescriptorEmitter()


class ClockSourceDescriptor(DescriptorContextManager):
    ParentDescriptor = HeaderDescriptorEmitter
    DescriptorEmitter = lambda self: ClockSourceDescriptorEmitter()


class PowerDomainDescriptor(DescriptorContextManager):
    ParentDescriptor = HeaderDescriptorEmitter
    DescriptorEmitter = lambda self: PowerDomainDescriptorEmitter()


class ClassSpecificAudioStreamingInterfaceDescriptor(DescriptorContextManager):
    ParentDescriptor = InterfaceDescriptorEmitter
    DescriptorEmitter = lambda self: ClassSpecificAudioStreamingInterfaceDescriptorEmitter()


class ConnectorDescriptor(DescriptorContextManager):
	ParentDescriptor = HeaderDescriptorEmitter
	DescriptorEmitter = lambda self: ConnectorDescriptorEmitter()

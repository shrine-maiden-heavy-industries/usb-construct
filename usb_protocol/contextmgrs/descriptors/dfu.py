#
# This file is part of usb-protocol.
#

from ..manager import DescriptorContextManager

from ...emitters.descriptors.standard import InterfaceDescriptorEmitter
from ...emitters.descriptors.dfu import FunctionalDescriptorEmitter


class FunctionalDescriptor(DescriptorContextManager):
    ParentDescriptor = InterfaceDescriptorEmitter
    DescriptorEmitter = lambda self: FunctionalDescriptorEmitter()

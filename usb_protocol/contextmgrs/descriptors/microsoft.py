#
# This file is part of usb-protocol.
#

from ..manager import DescriptorContextManager

from ...emitters.descriptors.standard import BinaryObjectStoreDescriptorEmitter
from ...emitters.descriptors.microsoft import PlatformDescriptorEmitter


class PlatformDescriptor(DescriptorContextManager):
    ParentDescriptor = BinaryObjectStoreDescriptorEmitter
    DescriptorEmitter = lambda self: PlatformDescriptorEmitter()

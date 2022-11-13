# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#

from ..manager import DescriptorContextManager

from ...emitters.descriptors.standard import BinaryObjectStoreDescriptorEmitter
from ...emitters.descriptors.microsoft import PlatformDescriptorEmitter, PlatformDescriptorCollection


class PlatformDescriptor(DescriptorContextManager):
    ParentDescriptor = BinaryObjectStoreDescriptorEmitter
    DescriptorEmitter = lambda self: PlatformDescriptorEmitter(platform_collection = self._platform_collection)

    def __init__(self, parentDesc : ParentDescriptor, platform_collection : PlatformDescriptorCollection):
        self._platform_collection = platform_collection
        super().__init__(parentDesc)

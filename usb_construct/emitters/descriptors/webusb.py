# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
"""
https://wicg.github.io/webusb/
"""


from ..           import emitter_for_format
from ..descriptor import ComplexDescriptorEmitter

from ...types.descriptors.webusb import *

URLDescriptorEmitter = emitter_for_format(URLDescriptor)

class PlatformDescriptorEmitter(ComplexDescriptorEmitter):

    DESCRIPTOR_FORMAT = PlatformDescriptor

    def _pre_emit(self):
        # Ensure that our landing page string is an index, if we can.
        if self._collection and hasattr(self, 'iLandingPage'):
            self.iLandingPage = self._collection.ensure_string_field_is_index(self.iLandingPage)

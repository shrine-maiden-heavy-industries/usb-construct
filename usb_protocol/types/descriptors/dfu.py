#
# This file is part of usb-protocol.
#
"""
Structures describing DFU USB descriptors. Versions that support parsing incomplete binary data
are available as `DescriptorType`.Partial, e.g. `DeviceDescriptor.Partial`, and are collectively available
in the `usb_protocol.types.descriptors.partial.dfu` module.
"""

from enum import IntEnum

import construct

from ..descriptor import \
    DescriptorField, DescriptorNumber, DescriptorFormat


class DFUDescriptorNumbers(IntEnum):
	FUNCTIONAL = 0x21


FunctionalDescriptor = DescriptorFormat(
	"bLength"             / construct.const(0x09, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(DFUDescriptorNumbers.FUNCTIONAL),
	"bmAttributes"        / DescriptorField("DFU Attributes", length = 1),
	"wDetachTimeOut"      / DescriptorField("Time, in miliseconds, that the device will wait after receipt of DFU_DETATCH to be asked to reset"),
	"wTransferSize"       / DescriptorField("Number of bytes (max) that the device can accept per control write"),
	"bcdDFUVersion"       / DescriptorField("Release version of the DFU spec this device conforms to", default = 1.1),
)

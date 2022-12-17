# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
'''
https://wicg.github.io/webusb/
'''

from enum import IntEnum

import construct
from construct    import len_, this

from ..descriptor import DescriptorField, DescriptorFormat, DescriptorNumber
from .standard    import DeviceCapabilityTypes, StandardDescriptorNumbers


class WebUSBRequestTypes(IntEnum):
	GET_URL = 2

class WebUSBDescriptorNumbers(IntEnum):
	WEBUSB_URL = 3

class WebUSBURLSchemaTypes(IntEnum):
	HTTP = 0,
	HTTPS = 1,

	EMPTY = 255

PlatformDescriptor = DescriptorFormat(
	'bLength'                / construct.Const(0x18, construct.Int8ul),
	'bDescriptorType'        / DescriptorNumber(StandardDescriptorNumbers.DEVICE_CAPABILITY),
	'bDevCapabilityType'     / DescriptorNumber(DeviceCapabilityTypes.PLATFORM),
	'bReserved'              / construct.Const(0x00, construct.Int8ul),
	'PlatformCapabilityUUID' / construct.Sequence(
			construct.Const(0x3408b638, construct.Int32ul),
			construct.Const(0x09a9,     construct.Int16ul),
			construct.Const(0x47a0,     construct.Int16ul),
			construct.Const(0x8bfd,     construct.Int16ub),
			construct.Const(0xa076,     construct.Int16ub),
			construct.Const(0x8815b665, construct.Int32ub)
		),
	'bcdVersion'             / DescriptorField('WebUSB Version', default = 1.0),
	'bVendorCode'            / DescriptorField('WebUSB Vendor Code', default = 1),
	'iLandingPage'           / DescriptorField('WebUSB Landing Page', default = 0),
)

URLDescriptor = DescriptorFormat(
	'bLength'         / construct.Rebuild(construct.Int8ul, len_(this.URL) + 3),
	'bDescriptorType' / DescriptorNumber(WebUSBDescriptorNumbers.WEBUSB_URL),
	'bScheme'         / DescriptorField('WebUSB URL Schema', default = WebUSBURLSchemaTypes.HTTPS),
	'URL'             / construct.CString('utf8'),
)

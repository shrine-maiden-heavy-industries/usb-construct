# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
'''
Structures describing DFU USB descriptors. Versions that support parsing incomplete binary data
are available as `DescriptorType`.Partial, e.g. `DeviceDescriptor.Partial`, and are collectively available
in the `usb_construct.types.descriptors.partial.dfu` module.
'''

from enum         import IntEnum

import construct

from ..descriptor import DescriptorField, DescriptorFormat, DescriptorNumber

class DFUDescriptorNumbers(IntEnum):
	FUNCTIONAL = 0x21


class DFUWillDetach(IntEnum):
	NO  = 0x00
	YES = 0x08


class DFUManifestationTolerant(IntEnum):
	NO  = 0
	YES = 0x04


class DFUCanUpload(IntEnum):
	NO  = 0
	YES = 0x02


class DFUCanDownload(IntEnum):
	NO  = 0
	YES = 0x01


class DFURequests(IntEnum):
	DETACH     = 0
	DOWNLOAD   = 1
	UPLOAD     = 2
	GET_STATUS = 3
	CLR_STATUS = 4
	GET_STATE  = 5
	ABORT      = 6


FunctionalDescriptor = DescriptorFormat(
	'bLength'         / construct.Const(0x09, construct.Int8ul),
	'bDescriptorType' / DescriptorNumber(DFUDescriptorNumbers.FUNCTIONAL),
	'bmAttributes'    / DescriptorField('DFU Attributes', length = 1),
	'wDetachTimeOut'  / DescriptorField(
		'Time, in milliseconds, that the device will wait after receipt of DFU_DETACH to be asked to reset'
	),
	'wTransferSize'   / DescriptorField('Number of bytes (max) that the device can accept per control write'),
	'bcdDFUVersion'   / DescriptorField('Release version of the DFU spec this device conforms to', default = 1.1),
)

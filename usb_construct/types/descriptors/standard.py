# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
'''
Structures describing standard USB descriptors. Versions that support parsing incomplete binary data
are available as `DescriptorType`.Partial, e.g. `DeviceDescriptor.Partial`, and are collectively available
in the `usb_construct.types.descriptors.partial.standard` module (which, like the structs in this module,
can also be imported without `.standard`).
'''

from enum         import IntEnum

import construct
from construct    import this

from ..descriptor import DescriptorField, DescriptorFormat, DescriptorNumber

class StandardDescriptorNumbers(IntEnum):
	''' Numbers of our standard descriptors. '''

	DEVICE                                        = 1
	CONFIGURATION                                 = 2
	STRING                                        = 3
	INTERFACE                                     = 4
	ENDPOINT                                      = 5
	DEVICE_QUALIFIER                              = 6
	OTHER_SPEED_DESCRIPTOR                        = 7
	OTHER_SPEED                                   = 7
	INTERFACE_POWER                               = 8
	OTG                                           = 9
	DEBUG                                         = 10
	INTERFACE_ASSOCIATION                         = 11

	# SuperSpeed only
	BOS                                           = 15
	DEVICE_CAPABILITY                             = 16
	SUPERSPEED_USB_ENDPOINT_COMPANION             = 48
	SUPERSPEEDPLUS_ISOCHRONOUS_ENDPOINT_COMPANION = 49


class DeviceCapabilityTypes(IntEnum):
	''' Numbers for the SuperSpeed standard Device Capabilities. '''

	WIRELESS_USB                = 1
	USB_2_EXTENSION             = 2
	SUPERSPEED_USB              = 3
	CONTAINER_ID                = 4
	PLATFORM                    = 5
	POWER_DELIVERY_CAPABILITY   = 6
	BATTERY_INFO_CAPABILITY     = 7
	PD_CONSUMER_PORT_CAPABILITY = 8
	PD_PROVIDER_PORT_CAPABILITY = 9
	SUPERSPEED_PLUS             = 10
	PRECISION_TIME_MEASUREMENT  = 11
	WIRELESS_USB_EXTENSION      = 12
	BILLBOARD                   = 13
	AUTHENTICATION              = 14
	BILLBOARD_EXTENSION         = 15
	CONFIGURATION_SUMMARY       = 16


class DeviceClassCodes(IntEnum):
	INTERFACE     = 0
	CDC           = 2
	HUB           = 9
	BILLBOARD     = 11
	DIAGNOSTIC    = 220
	MISCELLANEOUS = 239
	VENDOR        = 255


class InterfaceClassCodes(IntEnum):
	AUDIO               = 1
	CDC                 = 2
	HID                 = 3
	PHYSICAL            = 5
	IMAGE               = 6
	PRINTER             = 7
	MASS_STORAGE        = 8
	CDC_DATA            = 10
	SMART_CARD          = 11
	CONTENT_SECURITY    = 13
	VIDEO               = 14
	PERSONAL_HEALTHCARE = 15
	AUDIO_VIDEO         = 16
	TYPE_C_BRIDGE       = 18
	I3C_DEVICE          = 60
	DIAGNOSTIC          = 220
	WIRELESS            = 224
	MISCELLANEOUS       = 239
	APPLICATION         = 254
	VENDOR              = 255


class MassStorageSubclassCodes(IntEnum):
	NON_SPECIFIC = 0
	RBC          = 1
	MMC5_ATAPI   = 2
	QIC157       = 3
	UFI          = 4
	SFF8070i     = 5
	TRANSPARENT  = 6
	LSD_FS       = 7
	IEEE1667     = 8
	VENDOR       = 255


class MassStorageProtocolCodes(IntEnum):
	CBI_INTERRUPT    = 0
	CBI_NO_INTERRUPT = 1
	BBB              = 80
	UAS              = 98
	VENDOR           = 255


class MiscellaneousSubclassCodes(IntEnum):
	MULTIFUNCTION = 2


class MultifunctionProtocolCodes(IntEnum):
	INTERFACE_ASSOCIATION = 1


class ApplicationSubclassCodes(IntEnum):
	DFU = 1


class DFUProtocolCodes(IntEnum):
	APPLICATION = 1
	DFU         = 2


DeviceDescriptor = DescriptorFormat(
	'bLength'            / construct.Const(0x12, construct.Int8ul),
	'bDescriptorType'    / DescriptorNumber(StandardDescriptorNumbers.DEVICE),
	'bcdUSB'             / DescriptorField('USB Version', default = 2.0),
	'bDeviceClass'       / DescriptorField('Class',    default = 0),
	'bDeviceSubclass'    / DescriptorField('Subclass', default = 0),
	'bDeviceProtocol'    / DescriptorField('Protocol', default = 0),
	'bMaxPacketSize0'    / DescriptorField('EP0 Max Pkt Size', default = 64),
	'idVendor'           / DescriptorField('Vendor ID'),
	'idProduct'          / DescriptorField('Product ID'),
	'bcdDevice'          / DescriptorField('Device Version', default = 0),
	'iManufacturer'      / DescriptorField('Manufacturer Str', default = 0),
	'iProduct'           / DescriptorField('Product Str', default = 0),
	'iSerialNumber'      / DescriptorField('Serial Number', default = 0),
	'bNumConfigurations' / DescriptorField('Configuration Count'),
)


ConfigurationDescriptor = DescriptorFormat(
	'bLength'             / construct.Const(9, construct.Int8ul),
	'bDescriptorType'     / DescriptorNumber(StandardDescriptorNumbers.CONFIGURATION),
	'wTotalLength'        / DescriptorField('Length including subordinates'),
	'bNumInterfaces'      / DescriptorField('Interface count'),
	'bConfigurationValue' / DescriptorField('Configuration number', default = 1),
	'iConfiguration'      / DescriptorField('Description string', default = 0),
	'bmAttributes'        / DescriptorField('Attributes', default = 0x80),
	'bMaxPower'           / DescriptorField('Max power consumption', default = 250),
)

# Field that automatically reflects a string descriptor's length.
StringDescriptorLength = construct.Rebuild(
	construct.Int8ul, construct.len_(this.bString) * 2 + 2
)

StringDescriptor = DescriptorFormat(
	'bLength'         / StringDescriptorLength,
	'bDescriptorType' / DescriptorNumber(StandardDescriptorNumbers.STRING),
	'bString'         / construct.GreedyString('utf_16_le')
)


StringLanguageDescriptorLength = construct.Rebuild(
	construct.Int8ul, construct.len_(this.wLANGID) * 2 + 2
)

StringLanguageDescriptor = DescriptorFormat(
	'bLength'         / StringLanguageDescriptorLength,
	'bDescriptorType' / DescriptorNumber(StandardDescriptorNumbers.STRING),
	'wLANGID'         / construct.GreedyRange(construct.Int16ul)
)


InterfaceDescriptor = DescriptorFormat(
	'bLength'            / construct.Const(9, construct.Int8ul),
	'bDescriptorType'    / DescriptorNumber(StandardDescriptorNumbers.INTERFACE),
	'bInterfaceNumber'   / DescriptorField('Interface number'),
	'bAlternateSetting'  / DescriptorField('Alternate setting', default = 0),
	'bNumEndpoints'      / DescriptorField('Endpoints included'),
	'bInterfaceClass'    / DescriptorField('Class', default = 0xff),
	'bInterfaceSubclass' / DescriptorField('Subclass', default = 0xff),
	'bInterfaceProtocol' / DescriptorField('Protocol', default = 0xff),
	'iInterface'         / DescriptorField('String index', default = 0),
)


EndpointDescriptor = DescriptorFormat(

	# [USB2.0: 9.6; USB Audio Device Class Definition 1.0: 4.6.1.1, 4.6.2.1]
	# Interfaces of the Audio 1.0 class extend their subordinate endpoint descriptors with
	# 2 additional bytes (extending it from 7 to 9 bytes). Thankfully, this is the only extension that
	# changes the length of a standard descriptor type, but we do have to handle this case in Construct.
	'bLength'          / construct.Default(construct.OneOf(construct.Int8ul, [7, 9]), 7),
	'bDescriptorType'  / DescriptorNumber(StandardDescriptorNumbers.ENDPOINT),
	'bEndpointAddress' / DescriptorField('Endpoint Address'),
	'bmAttributes'     / DescriptorField('Attributes', default = 2),
	'wMaxPacketSize'   / DescriptorField('Maximum Packet Size', default = 64),
	'bInterval'        / DescriptorField('Polling interval', default = 255),

	# 2 bytes that are only present on endpoint descriptors for Audio 1.0 class interfaces.
	('bRefresh'        / construct.Optional(construct.Int8ul)) * 'Refresh Rate',
	('bSynchAddress'   / construct.Optional(construct.Int8ul)) * 'Synch Endpoint Address',
)


DeviceQualifierDescriptor = DescriptorFormat(
	'bLength'            / construct.Const(9, construct.Int8ul),
	'bDescriptorType'    / DescriptorNumber(StandardDescriptorNumbers.DEVICE_QUALIFIER),
	'bcdUSB'             / DescriptorField('USB Version'),
	'bDeviceClass'       / DescriptorField('Class'),
	'bDeviceSubclass'    / DescriptorField('Subclass'),
	'bDeviceProtocol'    / DescriptorField('Protocol'),
	'bMaxPacketSize0'    / DescriptorField('EP0 Max Pkt Size'),
	'bNumConfigurations' / DescriptorField('Configuration Count'),
	'_bReserved'         / construct.Optional(construct.Const(b'\0'))
)


InterfaceAssociationDescriptor = DescriptorFormat(
	'bLength'           / construct.Const(8, construct.Int8ul),
	'bDescriptorType'   / DescriptorNumber(StandardDescriptorNumbers.INTERFACE_ASSOCIATION),
	'bFirstInterface'   / DescriptorField(
		'Interface number of the first interface that is associated with this function.',
		default = 0
	),
	'bInterfaceCount'   / DescriptorField('Number of contiguous interfaces that are associated with this function'),
	'bFunctionClass'    / DescriptorField('Function class code'),
	'bFunctionSubclass' / DescriptorField('Function subclass code'),
	'bFunctionProtocol' / DescriptorField('Function protocol code'),
	'iFunction'         / DescriptorField('Index of a string descriptor that describes this interface', default = 0),
)


#
# SuperSpeed descriptors
#
BinaryObjectStoreDescriptor = DescriptorFormat(
	'bLength'         / construct.Const(0x5, construct.Int8ul),
	'bDescriptorType' / DescriptorNumber(StandardDescriptorNumbers.BOS),
	'wTotalLength'    / DescriptorField('Total Length', default = 5),
	'bNumDeviceCaps'  / DescriptorField('Device Capability Descriptors', default = 0),
)

USB2ExtensionDescriptor = DescriptorFormat(
	'bLength'            / construct.Const(0x7, construct.Int8ul),
	'bDescriptorType'    / DescriptorNumber(StandardDescriptorNumbers.DEVICE_CAPABILITY),
	'bDevCapabilityType' / construct.Const(DeviceCapabilityTypes.USB_2_EXTENSION, construct.Int8ul),
	'bmAttributes'       / DescriptorField('Attributes', default = 0b10, length = 4)
)

SuperSpeedUSBDeviceCapabilityDescriptor = DescriptorFormat(
	'bLength'               / construct.Const(0xA, construct.Int8ul),
	'bDescriptorType'       / DescriptorNumber(StandardDescriptorNumbers.DEVICE_CAPABILITY),
	'bDevCapabilityType'    / construct.Const(DeviceCapabilityTypes.SUPERSPEED_USB, construct.Int8ul),
	'bmAttributes'          / DescriptorField('Attributes', default = 0),
	'wSpeedsSupported'      / DescriptorField('USB3 Speeds Supported', default = 0b1000),
	'bFunctionalitySupport' / DescriptorField('Lowest Speed with Full Support', default = 3),
	'bU1DevExitLat'         / DescriptorField('U1 Exit Latency', default = 0),
	'wU2DevExitLat'         / DescriptorField('U2 Exit Latency', default = 0)
)


SuperSpeedEndpointCompanionDescriptor = DescriptorFormat(
	'bLength'           / construct.Const(0x6, construct.Int8ul),
	'bDescriptorType'   / DescriptorNumber(StandardDescriptorNumbers.SUPERSPEED_USB_ENDPOINT_COMPANION),
	'bMaxBurst'         / DescriptorField('Maximum Burst Length', default = 0),
	'bmAttributes'      / DescriptorField('Extended Attributes', default = 0),
	'wBytesPerInterval' / DescriptorField('Bytes Per Service Interval', default = 0),
)

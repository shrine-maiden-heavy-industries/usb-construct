# SPDX-License-Identifier: BSD-3-Clause

from .standard import (
	get_string_descriptor,

	InterfaceAssociationDescriptorEmitter, EndpointDescriptorEmitter,
	InterfaceDescriptorEmitter, ConfigurationDescriptorEmitter,
	DeviceDescriptorCollection, BinaryObjectStoreDescriptorEmitter,
	SuperSpeedDeviceDescriptorCollection,

	DeviceDescriptorEmitter, StringDescriptorEmitter, StringLanguageDescriptorEmitter,
	DeviceQualifierDescriptor, USB2ExtensionDescriptorEmitter,
	SuperSpeedUSBDeviceCapabilityDescriptorEmitter,
	SuperSpeedEndpointCompanionDescriptorEmitter,
)

__all__ = (
	'get_string_descriptor',

	'InterfaceAssociationDescriptorEmitter',
	'EndpointDescriptorEmitter',
	'InterfaceDescriptorEmitter',
	'ConfigurationDescriptorEmitter',
	'DeviceDescriptorCollection',
	'BinaryObjectStoreDescriptorEmitter',
	'SuperSpeedDeviceDescriptorCollection',

	'DeviceDescriptorEmitter',
	'StringDescriptorEmitter',
	'StringLanguageDescriptorEmitter',
	'DeviceQualifierDescriptor',
	'USB2ExtensionDescriptorEmitter',
	'SuperSpeedUSBDeviceCapabilityDescriptorEmitter',
	'SuperSpeedEndpointCompanionDescriptorEmitter',
)

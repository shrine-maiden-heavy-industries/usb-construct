# SPDX-License-Identifier: BSD-3-Clause

from .standard import (
	BinaryObjectStoreDescriptorEmitter, ConfigurationDescriptorEmitter, DeviceDescriptorCollection,
	DeviceDescriptorEmitter, DeviceQualifierDescriptorEmitter, EndpointDescriptorEmitter,
	InterfaceAssociationDescriptorEmitter, InterfaceDescriptorEmitter, StringDescriptorEmitter,
	StringLanguageDescriptorEmitter, SuperSpeedDeviceDescriptorCollection,
	SuperSpeedEndpointCompanionDescriptorEmitter, SuperSpeedUSBDeviceCapabilityDescriptorEmitter,
	USB2ExtensionDescriptorEmitter, get_string_descriptor,
)

__all__ = (
	'BinaryObjectStoreDescriptorEmitter',
	'ConfigurationDescriptorEmitter',
	'DeviceDescriptorCollection',
	'DeviceDescriptorEmitter',
	'DeviceQualifierDescriptorEmitter',
	'EndpointDescriptorEmitter',
	'InterfaceAssociationDescriptorEmitter',
	'InterfaceDescriptorEmitter',
	'StringDescriptorEmitter',
	'StringLanguageDescriptorEmitter',
	'SuperSpeedDeviceDescriptorCollection',
	'SuperSpeedEndpointCompanionDescriptorEmitter',
	'SuperSpeedUSBDeviceCapabilityDescriptorEmitter',
	'USB2ExtensionDescriptorEmitter',
	'get_string_descriptor',
)

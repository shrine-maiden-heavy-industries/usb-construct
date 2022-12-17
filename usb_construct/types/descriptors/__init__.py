# SPDX-License-Identifier: BSD-3-Clause

from .standard import (
	StandardDescriptorNumbers, DeviceCapabilityTypes, DeviceClassCodes,
	InterfaceClassCodes, MassStorageSubclassCodes,
	MassStorageProtocolCodes, MiscellaneousSubclassCodes,
	MultifunctionProtocolCodes, ApplicationSubclassCodes, DFUProtocolCodes,

	DeviceDescriptor, ConfigurationDescriptor, StringDescriptorLength,
	StringDescriptor, StringLanguageDescriptorLength, StringLanguageDescriptor,
	InterfaceDescriptor, EndpointDescriptor, DeviceQualifierDescriptor,
	InterfaceAssociationDescriptor, BinaryObjectStoreDescriptor, USB2ExtensionDescriptor,
	SuperSpeedUSBDeviceCapabilityDescriptor, SuperSpeedEndpointCompanionDescriptor,
)

__all__ = (
	'StandardDescriptorNumbers',
	'DeviceCapabilityTypes',
	'DeviceClassCodes',
	'InterfaceClassCodes',
	'MassStorageSubclassCodes',
	'MassStorageProtocolCodes',
	'MiscellaneousSubclassCodes',
	'MultifunctionProtocolCodes',
	'ApplicationSubclassCodes',
	'DFUProtocolCodes',

	'DeviceDescriptor',
	'ConfigurationDescriptor',
	'StringDescriptorLength',
	'StringDescriptor',
	'StringLanguageDescriptorLength',
	'StringLanguageDescriptor',
	'InterfaceDescriptor',
	'EndpointDescriptor',
	'DeviceQualifierDescriptor',
	'InterfaceAssociationDescriptor',
	'BinaryObjectStoreDescriptor',
	'USB2ExtensionDescriptor',
	'SuperSpeedUSBDeviceCapabilityDescriptor',
	'SuperSpeedEndpointCompanionDescriptor',
)

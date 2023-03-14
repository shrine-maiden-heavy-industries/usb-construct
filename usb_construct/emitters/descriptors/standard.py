# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
''' Convenience emitters for simple, standard descriptors. '''

from contextlib                    import contextmanager
from typing                        import Generator, Optional, List, Tuple, Union

from ...types                      import LanguageIDs
from ...types.descriptors.standard import *
from ..                            import ConstructEmitter, emitter_for_format
from ..descriptor                  import ComplexDescriptorEmitter

# Create our basic emitters...
DeviceDescriptorEmitter          = emitter_for_format(DeviceDescriptor)
StringDescriptorEmitter          = emitter_for_format(StringDescriptor)
StringLanguageDescriptorEmitter  = emitter_for_format(StringLanguageDescriptor)
DeviceQualifierDescriptorEmitter = emitter_for_format(DeviceQualifierDescriptor)

# ... our basic superspeed emitters ...
USB2ExtensionDescriptorEmitter                 = emitter_for_format(
	USB2ExtensionDescriptor
)
SuperSpeedUSBDeviceCapabilityDescriptorEmitter = emitter_for_format(
	SuperSpeedUSBDeviceCapabilityDescriptor
)
SuperSpeedEndpointCompanionDescriptorEmitter   = emitter_for_format(
	SuperSpeedEndpointCompanionDescriptor
)

# ... convenience functions ...
def get_string_descriptor(string: str) -> bytes:
	''' Generates a string descriptor for the relevant string. '''

	emitter = StringDescriptorEmitter()
	emitter.bString = string
	return emitter.emit()

# ... and complex emitters.
class InterfaceAssociationDescriptorEmitter(ComplexDescriptorEmitter):
	''' Emitter that creates an InterfaceAssociationDescriptor. '''

	DESCRIPTOR_FORMAT = InterfaceAssociationDescriptor

	def _pre_emit(self) -> None:
		# Ensure that our function string is an index, if we can.
		if self._collection and hasattr(self, 'iFunction'):
			self.iFunction = self._collection.ensure_string_field_is_index(self.iFunction)

class EndpointDescriptorEmitter(ComplexDescriptorEmitter):
	''' Emitter that creates an EndpointDescriptor. '''

	DESCRIPTOR_FORMAT = EndpointDescriptor

	@contextmanager
	def SuperSpeedCompanion(self) -> Generator[ConstructEmitter, None, None]:
		'''
		Context manager that allows addition of a SuperSpeed Companion to this endpoint descriptor.

		It can be used with a `with` statement; and yields an SuperSpeedEndpointCompanionDescriptorEmitter
		that can be populated:

		.. code-block:: python

			with endpoint.SuperSpeedEndpointCompanion() as d:
				d.bMaxBurst = 1

		This adds the relevant descriptor, automatically.

		'''

		descriptor = SuperSpeedEndpointCompanionDescriptorEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


class InterfaceDescriptorEmitter(ComplexDescriptorEmitter):
	''' Emitter that creates an InterfaceDescriptor. '''

	DESCRIPTOR_FORMAT = InterfaceDescriptor

	@contextmanager
	def EndpointDescriptor(self, *, add_default_superspeed: bool = False) -> Generator[EndpointDescriptorEmitter, None, None]:
		'''
		Context manager that allows addition of a subordinate endpoint descriptor.

		It can be used with a `with` statement; and yields an EndpointDescriptorEmitter
		that can be populated:

		.. code-block:: python

			with interface.EndpointDescriptor() as d:
				d.bEndpointAddress = 0x01
				d.bmAttributes     = 0x80
				d.wMaxPacketSize   = 64
				d.bInterval        = 0

		This adds the relevant descriptor, automatically.

		'''

		descriptor = EndpointDescriptorEmitter()
		yield descriptor

		# If we're adding a default SuperSpeed extension, do so.
		if add_default_superspeed:
			with descriptor.SuperSpeedCompanion():
				pass

		self.add_subordinate_descriptor(descriptor)


	def _pre_emit(self) -> None:

		# Count our endpoints, and update our internal count.
		self.bNumEndpoints = self._type_counts[StandardDescriptorNumbers.ENDPOINT]

		# Ensure that our interface string is an index, if we can.
		if self._collection and hasattr(self, 'iInterface'):
			self.iInterface = self._collection.ensure_string_field_is_index(self.iInterface)



class ConfigurationDescriptorEmitter(ComplexDescriptorEmitter):
	''' Emitter that creates a configuration descriptor. '''

	DESCRIPTOR_FORMAT = ConfigurationDescriptor

	@contextmanager
	def InterfaceDescriptor(self) -> Generator[InterfaceDescriptorEmitter, None, None]:
		'''
		Context manager that allows addition of a subordinate interface descriptor.

		It can be used with a `with` statement; and yields an InterfaceDescriptorEmitter
		that can be populated:

		.. code-block:: python

			with interface.InterfaceDescriptor() as d:
				d.bInterfaceNumber = 0x01
				[snip]

		This adds the relevant descriptor, automatically. Note that populating derived
		fields such as bNumEndpoints aren't necessary; they'll be populated automatically.

		'''

		descriptor = InterfaceDescriptorEmitter(collection = self._collection)
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	@contextmanager
	def InterfaceAssociationDescriptor(self) -> Generator[InterfaceAssociationDescriptorEmitter, None, None]:
		'''
		Context manager that allows addition of a subordinate interface association descriptor.

		It can be used with a `with` statement; and yields an InterfaceAssociationDescriptorEmitter
		that can be populated:

		.. code-block:: python

			with interface.InterfaceAssociationDescriptor() as d:
				d.bFirstInterface = 0
				[snip]

		This adds the relevant descriptor, automatically.

		'''

		descriptor = InterfaceAssociationDescriptorEmitter(collection = self._collection)
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	def _pre_emit(self) -> None:

		# Count our interfaces. Alternate settings of the same interface do not count multiple times.
		self.bNumInterfaces = len(set([
			subordinate[2] for subordinate in self._subordinates if (subordinate[1] == StandardDescriptorNumbers.INTERFACE)
		]))

		# Figure out our total length.
		subordinate_length = sum(len(sub) for sub in self._subordinates)
		self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

		# Ensure that our configuration string is an index, if we can.
		if self._collection and hasattr(self, 'iConfiguration'):
			self.iConfiguration = self._collection.ensure_string_field_is_index(self.iConfiguration)



class DeviceDescriptorCollection:
	''' Object that builds a full collection of descriptors related to a given USB device. '''

	# Most systems seem happiest with en_US (ugh), so default to that.
	DEFAULT_SUPPORTED_LANGUAGES = [ LanguageIDs.ENGLISH_US ]


	def __init__(self, automatic_language_descriptor: bool = True) -> None:
		'''
		Parameters
		----------
		automatic_language_descriptor : bool
			If set or not provided, a language descriptor will automatically
			be added if none exists.

		'''

		self._automatic_language_descriptor = automatic_language_descriptor

		# Create our internal descriptor tracker.
		# Keys are a tuple of (type, index).
		self._descriptors: dict[tuple[int, int], bytes] = {}

		# Track string descriptors as they're created.
		self._next_string_index = 1
		self._index_for_string: dict[str, int] = {}


	def ensure_string_field_is_index(self, field_value: Union[int, str]) -> int:
		'''
		Processes the given field value; if it's not an string index, converts it to one.

		Non-index-fields are converted to indices using `get_index_for_string`, which automatically
		adds the relevant fields to our string descriptor collection.

		'''

		if isinstance(field_value, str):
			return self.get_index_for_string(field_value)
		else:
			return field_value


	def get_index_for_string(self, string: str) -> int:
		'''
		Returns an string descriptor index for the given string.

		If a string descriptor already exists for the given string, its index is
		returned. Otherwise, a string descriptor is created.

		'''

		# If we already have a descriptor for this string, return it.
		if string in self._index_for_string:
			return self._index_for_string[string]


		# Otherwise, create one:

		# Allocate an index...
		index = self._next_string_index
		self._index_for_string[string] = index
		self._next_string_index += 1

		# ... store our string descriptor with it ...
		identifier = StandardDescriptorNumbers.STRING, index
		self._descriptors[identifier] = get_string_descriptor(string)

		# ... and return our index.
		return index


	def add_descriptor(self, descriptor, index: int = 0, descriptor_type = None) -> None:
		'''
		Adds a descriptor to our collection.

		Parameters
		----------
		descriptor
			The descriptor to be added.

		index
			The index of the relevant descriptor. Defaults to 0.

		descriptor_type
			The type of the descriptor to be added. If `None`,
			this is automatically derived from the descriptor contents.

		'''

		# If this is an emitter rather than a descriptor itself, convert it.
		if hasattr(descriptor, 'emit'):
			descriptor: bytes = descriptor.emit()

		# Figure out the identifier (type + index) for this descriptor...
		if (descriptor_type is None):
			descriptor_type = descriptor[1]
		identifier = descriptor_type, index

		# ... and store it.
		self._descriptors[identifier] = descriptor


	def add_language_descriptor(self, supported_languages: Optional[List[LanguageIDs]] = None):
		'''
		Adds a language descriptor to the list of device descriptors.

		Parameters
		----------
		supported_languages : List[LanguageIDs]
			A list of languages supported by the device.

		'''

		if supported_languages is None:
			supported_languages = self.DEFAULT_SUPPORTED_LANGUAGES

		descriptor = StringLanguageDescriptorEmitter()
		descriptor.wLANGID = supported_languages
		self.add_descriptor(descriptor)


	@contextmanager
	def DeviceDescriptor(self) -> Generator[ConstructEmitter, None, None] :
		'''
		Context manager that allows addition of a device descriptor.

		It can be used with a `with` statement; and yields an DeviceDescriptorEmitter
		that can be populated:

		.. code-block:: python

			with collection.DeviceDescriptor() as d:
				d.idVendor  = 0xabcd
				d.idProduct = 0x1234
				[snip]

		This adds the relevant descriptor, automatically.

		'''

		descriptor = DeviceDescriptorEmitter()
		yield descriptor

		# If we have any string fields, ensure that they're indices before continuing.
		for field in ('iManufacturer', 'iProduct', 'iSerialNumber'):
			if hasattr(descriptor, field):
				value = getattr(descriptor, field)
				index = self.ensure_string_field_is_index(value)
				setattr(descriptor, field, index)

		self.add_descriptor(descriptor)


	@contextmanager
	def ConfigurationDescriptor(self) -> Generator[ConfigurationDescriptorEmitter, None, None]:
		'''
		Context manager that allows addition of a configuration descriptor.

		It can be used with a `with` statement; and yields an ConfigurationDescriptorEmitter
		that can be populated:

		.. code-block:: python

			with collection.ConfigurationDescriptor() as d:
				d.bConfigurationValue = 1
				[snip]

		This adds the relevant descriptor, automatically. Note that populating derived
		fields such as bNumInterfaces aren't necessary; they'll be populated automatically.

		'''

		descriptor = ConfigurationDescriptorEmitter(collection = self)
		yield descriptor

		self.add_descriptor(descriptor)


	@contextmanager
	def BOSDescriptor(self) -> Generator['BinaryObjectStoreDescriptorEmitter', None, None]:
		'''
		Context manager that allows addition of a Binary Object Store descriptor.

		It can be used with a `with` statement; and yields an BinaryObjectStoreDescriptorEmitter
		that can be populated:

		.. code-block:: python

			with collection.BOSDescriptor() as d:
				[snip]

		This adds the relevant descriptor, automatically. Note that populating derived
		fields such as bNumDeviceCaps aren't necessary; they'll be populated automatically.

		'''

		descriptor = BinaryObjectStoreDescriptorEmitter()
		yield descriptor

		self.add_descriptor(descriptor)


	def _ensure_has_language_descriptor(self) -> None:
		''' ensures that we have a language descriptor; adding one if necessary.'''

		# if we're not automatically adding a language descriptor, we shouldn't do anything,
		# and we'll just ignore this.
		if not self._automatic_language_descriptor:
			return

		# if we don't have a language descriptor, add our default one.
		if (StandardDescriptorNumbers.STRING, 0) not in self._descriptors:
			self.add_language_descriptor()



	def get_descriptor_bytes(self, type_number: int, index: int = 0) -> bytes:
		'''
		Returns the raw, binary descriptor for a given descriptor type/index.

		Parameters
		----------
		type_number : int
			The descriptor type number.

		index : int
			The index of the relevant descriptor, if relevant.

		'''

		# If this is a request for a language descriptor, return one.
		if (type_number, index) == (StandardDescriptorNumbers.STRING, 0):
			self._ensure_has_language_descriptor()

		return self._descriptors[(type_number, index)]


	def __iter__(self) -> Generator[Tuple[int, int, bytes], None, None]:
		''' Allow iterating over each of our descriptors; yields (index, value, descriptor). '''
		self._ensure_has_language_descriptor()
		return ((number, index, desc) for ((number, index), desc) in self._descriptors.items())




class BinaryObjectStoreDescriptorEmitter(ComplexDescriptorEmitter):
	''' Emitter that creates a BinaryObjectStore descriptor. '''

	DESCRIPTOR_FORMAT = BinaryObjectStoreDescriptor

	@contextmanager
	def USB2Extension(self) -> Generator[ConstructEmitter, None, None]:
		'''
		Context manager that allows addition of a USB 2.0 Extension to this Binary Object Store.

		It can be used with a `with` statement; and yields an USB2ExtensionDescriptorEmitter
		that can be populated:

		.. code-block:: python

			with bos.USB2Extension() as e:
				e.bmAttributes = 1

		This adds the relevant descriptor, automatically.

		'''

		descriptor = USB2ExtensionDescriptorEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	@contextmanager
	def SuperSpeedUSBDeviceCapability(self) -> Generator[ConstructEmitter, None, None]:
		'''
		Context manager that allows addition of a SS Device Capability to this Binary Object Store.

		It can be used with a `with` statement; and yields an SuperSpeedUSBDeviceCapabilityDescriptorEmitter
		that can be populated:

		.. code-block:: python


			with bos.SuperSpeedUSBDeviceCapability() as e:
				e.wSpeedSupported       = 0b1110
				e.bFunctionalitySupport = 1

		This adds the relevant descriptor, automatically.

		'''

		descriptor = SuperSpeedUSBDeviceCapabilityDescriptorEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	def _pre_emit(self) -> None:

		# Figure out the total length of our descriptor, including subordinates.
		subordinate_length = sum(len(sub) for sub in self._subordinates)
		self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

		# Count our subordinate descriptors, and update our internal count.
		self.bNumDeviceCaps = len(self._subordinates)



class SuperSpeedDeviceDescriptorCollection(DeviceDescriptorCollection):
	''' Object that builds a full collection of descriptors related to a given USB3 device. '''

	def __init__(self, automatic_descriptors: bool = True) -> None:
		'''
		Parameters
		-----------
		automatic_descriptors : bool
			If set or not provided, certain required descriptors will be
			be added if none exists.

		'''

		self._automatic_descriptors = automatic_descriptors
		super().__init__(automatic_language_descriptor = automatic_descriptors)


	def add_default_bos_descriptor(self) -> None:
		''' Adds a default, empty BOS descriptor. '''

		# Create an empty BOS descriptor...
		descriptor = BinaryObjectStoreDescriptorEmitter()

		# ... populate our default required descriptors...
		descriptor.add_subordinate_descriptor(USB2ExtensionDescriptorEmitter())
		descriptor.add_subordinate_descriptor(SuperSpeedUSBDeviceCapabilityDescriptorEmitter())

		# ... and add it to our overall BOS descriptor.
		self.add_descriptor(descriptor)


	def _ensure_has_bos_descriptor(self) -> None:
		''' Ensures that we have a BOS descriptor; adding one if necessary.'''

		# If we're not automatically adding a language descriptor, we shouldn't do anything,
		# and we'll just ignore this.
		if not self._automatic_descriptors:
			return

		# If we don't have a language descriptor, add our default one.
		if (StandardDescriptorNumbers.BOS, 0) not in self._descriptors:
			self.add_default_bos_descriptor()


	def __iter__(self) -> Generator[tuple[int, int, bytes], None, None]:
		''' Allow iterating over each of our descriptors; yields (index, value, descriptor). '''
		self._ensure_has_bos_descriptor()
		return super().__iter__()

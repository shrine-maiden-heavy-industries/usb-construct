# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
''' Convenience emitters for microsoft OS descriptors. '''

from contextlib                     import contextmanager
from typing                         import Generator

from ...types.descriptors.microsoft import *
from ..                             import emitter_for_format
from ..descriptor                   import ComplexDescriptorEmitter, ConstructEmitter

# Create our basic emitters...
FeatureCompatibleIDEmitter   = emitter_for_format(FeatureCompatibleID)
FeatureRegPropertyEmitter    = emitter_for_format(FeatureRegProperty)
FeatureMinResumeTimeEmitter  = emitter_for_format(FeatureMinResumeTime)
FeatureModelIDEmitter        = emitter_for_format(FeatureModelID)
FeatureCCGPDeviceEmitter     = emitter_for_format(FeatureCCGPDevice)
FeatureVendorRevisionEmitter = emitter_for_format(FeatureVendorRevision)

# ... and complex emitters.
class FeatureDescriptorEmitter(ComplexDescriptorEmitter):
	''' Abstract base type for things that can hold Feature Descriptors. '''

	@contextmanager
	def FeatureCompatibleID(self) -> Generator[ConstructEmitter, None, None]:
		descriptor = FeatureCompatibleIDEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	@contextmanager
	def FeatureRegProperty(self) -> Generator[ConstructEmitter, None, None]:
		descriptor = FeatureRegPropertyEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	@contextmanager
	def FeatureMinResumeTime(self) -> Generator[ConstructEmitter, None, None]:
		descriptor = FeatureMinResumeTimeEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	@contextmanager
	def FeatureModelID(self) -> Generator[ConstructEmitter, None, None]:
		descriptor = FeatureModelIDEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	@contextmanager
	def FeatureCCGPDevice(self) -> Generator[ConstructEmitter, None, None]:
		descriptor = FeatureCCGPDeviceEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	@contextmanager
	def FeatureVendorRevision(self) -> Generator[ConstructEmitter, None, None]:
		descriptor = FeatureVendorRevisionEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


class SubsetHeaderFunctionEmitter(FeatureDescriptorEmitter):
	''' Emitter that creates a SubsetHeaderFunctionEmitter. '''

	DESCRIPTOR_FORMAT = SubsetHeaderFunction

	def _pre_emit(self) -> None:
		# Figure out our total length.
		subordinate_length = sum(len(sub) for sub in self._subordinates)
		self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()


class SubsetHeaderConfigurationEmitter(FeatureDescriptorEmitter):
	''' Emitter that creates a SubsetHeaderConfiguration. '''

	DESCRIPTOR_FORMAT = SubsetHeaderConfiguration

	@contextmanager
	def SubsetHeaderFunction(self) -> Generator[ConstructEmitter, None, None]:
		descriptor = SubsetHeaderFunctionEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	def _pre_emit(self) -> None:
		# Figure out our total length.
		subordinate_length = sum(len(sub) for sub in self._subordinates)
		self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()


class SetHeaderDescriptorEmitter(FeatureDescriptorEmitter):
	''' Emitter that creates a SetHeaderDescriptor. '''

	DESCRIPTOR_FORMAT = SetHeaderDescriptor

	@contextmanager
	def SubsetHeaderConfiguration(self) -> Generator[ConstructEmitter, None, None]:
		descriptor = SubsetHeaderConfigurationEmitter()
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	def _pre_emit(self) -> None:
		# Figure out our total length.
		subordinate_length = sum(len(sub) for sub in self._subordinates)
		self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()


class DescriptorSetInformationEmitter(ComplexDescriptorEmitter):
	''' Emitter that creates a DescriptorSetInformation. '''

	DESCRIPTOR_FORMAT = DescriptorSetInformation

	@contextmanager
	def SetHeaderDescriptor(self) -> Generator[ConstructEmitter, None, None]:
		assert hasattr(self, 'bMS_VendorCode')

		descriptor = SetHeaderDescriptorEmitter()
		yield descriptor

		self._subordinate = descriptor
		self._collection.add_descriptor(descriptor, vendor_code = self.bMS_VendorCode)


	def _pre_emit(self) -> None:
		# Figure out our total length.
		self.wMSOSDescriptorSetTotalLength = self._subordinate.wTotalLength


class PlatformDescriptorCollection:
	''' Object that holds the OS descriptor sets for windows '''

	def __init__(self) -> None:
		self._descriptors: dict[int, bytes] = {}


	def add_descriptor(self, descriptor: SetHeaderDescriptorEmitter, vendor_code: int) -> None:
		'''
		Adds a descriptor to our collection.

		Parameters
		----------
		descriptor
			The set header descriptor to be added.

		vendor_code : int
			The vendor request code for this descriptor tree

		'''

		assert isinstance(descriptor, SetHeaderDescriptorEmitter)
		descriptor = descriptor.emit()

		self._descriptors[vendor_code] = descriptor


	@property
	def descriptors(self) -> dict[int, bytes]:
		return self._descriptors


class PlatformDescriptorEmitter(ComplexDescriptorEmitter):
	''' Emitter that creates a PlatformDescriptor. '''

	DESCRIPTOR_FORMAT = PlatformDescriptor

	def __init__(
		self, platform_collection: PlatformDescriptorCollection, *args, **kwargs
	) -> None:
		super().__init__(*args, **kwargs)

		self._platform_collection = platform_collection


	@contextmanager
	def DescriptorSetInformation(self) -> Generator[ConstructEmitter, None, None]:
		'''
		Context manager that allows addition of the information associated with a descriptor set.

		It can be used with a `with` statement; and yields a DescriptorSetInformationEmitter
		that can be populated:

		.. code-block:: python

			with platformDescriptor.DescriptorSetInformation() as dsi:
				dsi.bMS_VendorCode = 1

		This adds the relevant descriptor, automatically.

		'''

		descriptor = DescriptorSetInformationEmitter(collection = self._platform_collection)
		yield descriptor

		self.add_subordinate_descriptor(descriptor)


	def _pre_emit(self) -> None:
		# Figure out our total length.
		subordinate_length = sum(len(sub) for sub in self._subordinates)
		self.bLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

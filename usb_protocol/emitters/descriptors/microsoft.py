#
# This file is part of usb_protocol.
#
""" Convenience emitters for microsoft OS descriptors. """

from contextlib import contextmanager

from ..           import emitter_for_format
from ..descriptor import ComplexDescriptorEmitter

from ...types.descriptors.microsoft import *


# Create our basic emitters...
FeatureCompatibleIDEmitter = emitter_for_format(FeatureCompatibleID)
FeatureRegPropertyEmitter = emitter_for_format(FeatureRegProperty)
FeatureMinResumeTimeEmitter = emitter_for_format(FeatureMinResumeTime)
FeatureModelIDEmitter = emitter_for_format(FeatureModelID)
FeatureCCGPDeviceEmitter = emitter_for_format(FeatureCCGPDevice)
FeatureVendorRevisionEmitter = emitter_for_format(FeatureVendorRevision)

# ... and complex emitters.
class FeatureDescriptorEmitter(ComplexDescriptorEmitter):
    """ Abstract base type for things that can hold Feature Descriptors. """

    @contextmanager
    def FeatureCompatibleID(self):
        descriptor = FeatureCompatibleIDEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    @contextmanager
    def FeatureRegProperty(self):
        descriptor = FeatureRegPropertyEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    @contextmanager
    def FeatureMinResumeTime(self):
        descriptor = FeatureMinResumeTimeEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    @contextmanager
    def FeatureModelID(self):
        descriptor = FeatureModelIDEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    @contextmanager
    def FeatureCCGPDevice(self):
        descriptor = FeatureCCGPDeviceEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    @contextmanager
    def FeatureVendorRevision(self):
        descriptor = FeatureVendorRevisionEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


class SubsetHeaderFunctionEmitter(FeatureDescriptorEmitter):
    """ Emitter that creates a SubsetHeaderFunctionEmitter. """

    DESCRIPTOR_FORMAT = SubsetHeaderFunction

    def _pre_emit(self):
        # Figure out our total length.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()


class SubsetHeaderConfigurationEmitter(FeatureDescriptorEmitter):
    """ Emitter that creates a SubsetHeaderConfiguration. """

    DESCRIPTOR_FORMAT = SubsetHeaderConfiguration

    @contextmanager
    def SubsetHeaderFunction(self):
        descriptor = SubsetHeaderFunctionEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    def _pre_emit(self):
        # Figure out our total length.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()


class SetHeaderDescriptorEmitter(FeatureDescriptorEmitter):
    """ Emitter that creates a SetHeaderDescriptor. """

    DESCRIPTOR_FORMAT = SetHeaderDescriptor

    @contextmanager
    def SubsetHeaderConfiguration(self):
        descriptor = SubsetHeaderConfigurationEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    def _pre_emit(self):
        # Figure out our total length.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()


class DescriptorSetInformationEmitter(ComplexDescriptorEmitter):
    """ Emitter that creates a DescriptorSetInformation. """

    DESCRIPTOR_FORMAT = DescriptorSetInformation

    @contextmanager
    def SetHeaderDescriptor(self):
        descriptor = SetHeaderDescriptorEmitter()
        yield descriptor

        self._subordinate = descriptor

        # TODO: Add descriptor to the BOS collection


    def _pre_emit(self):
        # Figure out our total length.
        self.wMSOSDescriptorSetTotalLength = self._subordinate.wTotalLength


class PlatformDescriptorEmitter(ComplexDescriptorEmitter):
    """ Emitter that creates a PlatformDescriptor. """

    DESCRIPTOR_FORMAT = PlatformDescriptor

    @contextmanager
    def DescriptorSetInformation(self):
        """ Context manager that allows addition of the information associated with a descriptor set.

        It can be used with a `with` statement; and yields a DescriptorSetInformationEmitter
        that can be populated:

            with platformDescriptor.DescriptorSetInformation() as dsi:
                dsi.bMS_VendorCode = 1

        This adds the relevant descriptor, automatically.
        """

        descriptor = DescriptorSetInformationEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    def _pre_emit(self):
        # Figure out our total length.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.bLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

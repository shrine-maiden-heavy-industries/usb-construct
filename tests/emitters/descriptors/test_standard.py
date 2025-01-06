# SPDX-License-Identifier: BSD-3-Clause

import unittest

from usb_construct.emitters.descriptors.standard import (
	get_string_descriptor,
	DeviceDescriptorCollection,
	StringDescriptorEmitter, ConfigurationDescriptorEmitter,
)

class EmitterTests(unittest.TestCase):

	def test_string_emitter(self):
		emitter = StringDescriptorEmitter()
		emitter.bString = 'Hello'

		self.assertEqual(emitter.emit(), b'\x0C\x03H\0e\0l\0l\0o\0')


	def test_string_emitter_function(self):
		self.assertEqual(get_string_descriptor('Hello'), b'\x0C\x03H\0e\0l\0l\0o\0')


	def test_configuration_emitter(self):
		descriptor = bytes([

			# config descriptor
			12,     # length
			2,      # type
			25, 00, # total length
			1,      # num interfaces
			1,      # configuration number
			0,      # config string
			0x80,   # attributes
			250,    # max power

			# interface descriptor
			9,    # length
			4,    # type
			0,    # number
			0,    # alternate
			1,    # num endpoints
			0xff, # class
			0xff, # subclass
			0xff, # protocol
			0,    # string

			# endpoint descriptor
			7,       # length
			5,       # type
			0x01,    # address
			2,       # attributes
			64, 0,   # max packet size
			255,     # interval
		])


		# Create a trivial configuration descriptor...
		emitter = ConfigurationDescriptorEmitter()

		with emitter.InterfaceDescriptor() as interface:
			interface.bInterfaceNumber = 0

			with interface.EndpointDescriptor() as endpoint:
				endpoint.bEndpointAddress = 1


		# ... and validate that it matches our reference descriptor.
		binary = emitter.emit()
		self.assertEqual(len(binary), len(descriptor))


	def test_descriptor_collection(self):
		collection = DeviceDescriptorCollection()

		with collection.DeviceDescriptor() as d:
			d.idVendor           = 0xdead
			d.idProduct          = 0xbeef
			d.bNumConfigurations = 1

			d.iManufacturer      = 'Test Company'
			d.iProduct           = 'Test Product'


		with collection.ConfigurationDescriptor() as c:
			c.bConfigurationValue = 1

			with c.InterfaceDescriptor() as i:
				i.bInterfaceNumber = 1

				with i.EndpointDescriptor() as e:
					e.bEndpointAddress = 0x81

				with i.EndpointDescriptor() as e:
					e.bEndpointAddress = 0x01


		results = list(collection)

		# We should wind up with four descriptor entries, as our endpoint/interface descriptors are
		# included in our configuration descriptor.
		self.assertEqual(len(results), 5)

		# Supported languages string.
		self.assertIn((3, 0, b'\x04\x03\x09\x04'), results)

		# Manufacturer / product string.
		self.assertIn((3, 1, b'\x1a\x03T\x00e\x00s\x00t\x00 \x00C\x00o\x00m\x00p\x00a\x00n\x00y\x00'), results)
		self.assertIn((3, 2, b'\x1a\x03T\x00e\x00s\x00t\x00 \x00P\x00r\x00o\x00d\x00u\x00c\x00t\x00'), results)

		# Device descriptor.
		self.assertIn((1, 0, b'\x12\x01\x00\x02\x00\x00\x00@\xad\xde\xef\xbe\x00\x00\x01\x02\x00\x01'), results)

		# Configuration descriptor, with subordinates.
		self.assertIn((2, 0,
			b'\t\x02 \x00\x01\x01\x00\x80\xfa\t\x04\x01\x00\x02\xff\xff\xff\x00\x07\x05\x81\x02@\x00\xff\x07\x05\x01\x02@\x00\xff'
		), results)


	def test_empty_descriptor_collection(self):
		collection = DeviceDescriptorCollection(automatic_language_descriptor = False)
		results = list(collection)
		self.assertEqual(len(results), 0)

	def test_automatic_language_descriptor(self):
		collection = DeviceDescriptorCollection(automatic_language_descriptor = True)
		results = list(collection)
		self.assertEqual(len(results), 1)

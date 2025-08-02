# SPDX-License-Identifier: BSD-3-Clause

import unittest

import construct
from usb_construct.types                      import LanguageIDs
from usb_construct.types.descriptor           import BCDFieldAdapter
from usb_construct.types.descriptors.standard import (
	DeviceDescriptor, StringDescriptor, StringLanguageDescriptor
)

class DescriptorParserCases(unittest.TestCase):

	STRING_DESCRIPTOR = bytes([
		40, # Length
		3,  # Type
		ord('G'), 0x00,
		ord('r'), 0x00,
		ord('e'), 0x00,
		ord('a'), 0x00,
		ord('t'), 0x00,
		ord(' '), 0x00,
		ord('S'), 0x00,
		ord('c'), 0x00,
		ord('o'), 0x00,
		ord('t'), 0x00,
		ord('t'), 0x00,
		ord(' '), 0x00,
		ord('G'), 0x00,
		ord('a'), 0x00,
		ord('d'), 0x00,
		ord('g'), 0x00,
		ord('e'), 0x00,
		ord('t'), 0x00,
		ord('s'), 0x00,
	])

	def test_string_descriptor_parse(self):

		# Parse the relevant string...
		parsed = StringDescriptor.parse(self.STRING_DESCRIPTOR)

		# ... and check the descriptor's fields.
		self.assertEqual(parsed.bLength,                    40)
		self.assertEqual(parsed.bDescriptorType,             3)
		self.assertEqual(parsed.bString, 'Great Scott Gadgets')

	def test_string_descriptor_build(self):
		data = StringDescriptor.build({
			'bString': 'Great Scott Gadgets'
		})

		self.assertEqual(data, self.STRING_DESCRIPTOR)

	def test_string_language_descriptor_build(self):
		data = StringLanguageDescriptor.build({
			'wLANGID': (LanguageIDs.ENGLISH_US,)
		})

		self.assertEqual(data, b'\x04\x03\x09\x04')

	def test_device_descriptor(self):

		device_descriptor = [
			0x12,         # Length
			0x01,         # Type
			0x00, 0x02,   # USB version
			0xFF,         # class
			0xFF,         # subclass
			0xFF,         # protocol
			64,           # ep0 max packet size
			0xd0, 0x16,   # VID
			0x3b, 0x0f,   # PID
			0x00, 0x00,   # device rev
			0x01,         # manufacturer string
			0x02,         # product string
			0x03,         # serial number
			0x01          # number of configurations
		]

		# Parse the relevant string...
		parsed = DeviceDescriptor.parse(device_descriptor)

		# ... and check the descriptor's fields.
		self.assertEqual(parsed.bLength,             18)
		self.assertEqual(parsed.bDescriptorType,      1)
		self.assertEqual(parsed.bcdUSB,             2.0)
		self.assertEqual(parsed.bDeviceClass,      0xFF)
		self.assertEqual(parsed.bDeviceSubclass,   0xFF)
		self.assertEqual(parsed.bDeviceProtocol,   0xFF)
		self.assertEqual(parsed.bMaxPacketSize0,     64)
		self.assertEqual(parsed.idVendor,        0x16d0)
		self.assertEqual(parsed.idProduct,       0x0f3b)
		self.assertEqual(parsed.bcdDevice,            0)
		self.assertEqual(parsed.iManufacturer,        1)
		self.assertEqual(parsed.iProduct,             2)
		self.assertEqual(parsed.iSerialNumber,        3)
		self.assertEqual(parsed.bNumConfigurations,   1)

	def test_bcd_constructor(self):

		emitter = BCDFieldAdapter(construct.Int16ul)
		result = emitter.build(1.4)

		self.assertEqual(result, b'\x40\x01')

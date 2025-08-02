# SPDX-License-Identifier: BSD-3-Clause

from unittest import TestCase

from usb_construct.types import USBDirection, USBRequestRecipient, USBRequestType

class USBTypesBitwise(TestCase):

	def test_build_bmreqtype(self):
		self.assertEqual(
			0xA1,
			USBDirection.IN | USBRequestType.CLASS | USBRequestRecipient.INTERFACE
		)

		self.assertEqual(
			0xC0,
			USBDirection.IN | USBRequestType.VENDOR | USBRequestRecipient.DEVICE
		)

		self.assertEqual(
			0x01,
			USBDirection.OUT | USBRequestType.STANDARD | USBRequestRecipient.INTERFACE
		)

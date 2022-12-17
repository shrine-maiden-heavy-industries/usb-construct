# SPDX-License-Identifier: BSD-3-Clause

import unittest
import construct

from usb_construct.emitters.construct_interop import (
	ConstructEmitter
)

class ConstructEmitterTest(unittest.TestCase):

	def test_simple_emitter(self):

		test_struct = construct.Struct(
			'a' / construct.Int8ul,
			'b' / construct.Int8ul
		)

		emitter   = ConstructEmitter(test_struct)
		emitter.a = 0xab
		emitter.b = 0xcd

		self.assertEqual(emitter.emit(), b'\xab\xcd')

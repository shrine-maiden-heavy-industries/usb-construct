# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
''' Helpers for creating construct-related emitters. '''

import construct

class ConstructEmitter:
	'''
	Class that creates a simple emitter based on a construct struct.


	Examples
	--------

	For example, if we have a construct format that looks like the following:

	.. code-block:: python

		MyStruct = struct(
			'a' / Int8
			'b' / Int8
		)

	We could create emit an object like follows:

	.. code-block:: python

		emitter   = ConstructEmitter(MyStruct)
		emitter.a = 0xab
		emitter.b = 0xcd
		my_bytes  = emitter.emit() # '\xab\xcd'


	'''

	def __init__(self, struct: construct.Struct) -> None:
		'''
		Parameters
		----------
		construct_format : construct.Struct
			The format for which to create an emitter.

		'''
		self.__dict__['format'] = struct
		self.__dict__['fields'] = {}


	def _format_contains_field(self, field_name: str) -> bool:
		'''
		Returns True iff the given format has a field with the provided name.

		Parameters
		----------
		format_object
			The Construct format to work with. This includes e.g. most descriptor types.

		field_name : str
			The field name to query.

		'''
		return any(f.name == field_name for f in self.format.subcons)


	def __setattr__(self, name: str, value) -> None:
		''' Hook that we used to set our fields. '''

		# If the field starts with a '_', don't handle it, as it's an internal field.
		if name.startswith('_'):
			super().__setattr__(name, value)
			return

		if not self._format_contains_field(name):
			raise AttributeError(f'emitter specification contains no field {name}')

		self.fields[name] = value


	def emit(self) -> bytes:
		''' Emits the stream of bytes associated with this object. '''

		try:
			return self.format.build(self.fields)
		except KeyError as e:
			raise KeyError(f'missing necessary field: {e}')


	def __getattr__(self, name: str):
		''' Retrieves an emitter field, if possible. '''

		if name in self.fields:
			return self.fields[name]
		else:
			raise AttributeError(f'descriptor emitter has no property {name}')


def emitter_for_format(construct_format: construct.Struct):
	''' Creates a factory method for the relevant construct format. '''

	def _factory() -> ConstructEmitter:
		return ConstructEmitter(construct_format)

	return _factory

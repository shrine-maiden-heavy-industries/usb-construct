# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#

from collections import defaultdict

from .           import ConstructEmitter

class ComplexDescriptorEmitter(ConstructEmitter):
	''' Base class for emitting complex descriptors, which contain nested subordinates. '''

	# Base classes should override this.
	DESCRIPTOR_FORMAT = None

	def __init__(self, collection = None) -> None:
		'''
		Parameters
		----------
		collection
			If this descriptor belongs to a collection, it should be
			provided here. Using a collection object allows e.g. automatic
			assignment of string descriptor indices.

		'''

		self._collection = collection

		# Always create a basic ConstructEmitter from the given format.
		super().__init__(self.DESCRIPTOR_FORMAT)

		# Store a list of subordinate descriptors, and a count of
		# subordinate descriptor types.
		self._subordinates = []
		self._type_counts = defaultdict(int)


	def add_subordinate_descriptor(self, subordinate) -> None:
		'''
		Adds a subordinate descriptor to the relevant descriptor.

		Parameters
		----------
		subordinate
			The subordinate descriptor to add; can be an emitter,
			or a bytes-like object.

		'''  # noqa: E101

		if hasattr(subordinate, 'emit'):
			subordinate = subordinate.emit()
		else:
			subordinate = bytes(subordinate)

		# The second byte of a given descriptor is always its type number.
		# Count this descriptor type...
		subordinate_type = subordinate[1]

		self._type_counts[subordinate_type] += 1

		# ... and add the relevant bytes to our list of subordinates.
		self._subordinates.append(subordinate)


	def _pre_emit(self) -> None:
		''' Performs any manipulations needed on this object before emission. '''
		pass


	def emit(self, include_subordinates: bool = True) -> bytes:
		'''
		Emit our descriptor.

		Parameters
		----------
		include_subordinates
			If true or not provided, any subordinate descriptors will be included.

		'''

		# Run any pre-emit hook code before we perform our emission...
		self._pre_emit()

		# Start with our core descriptor...
		result = bytearray()
		result.extend(super().emit())

		# ... and if described, add our subordinates...
		for sub in self._subordinates:
			result.extend(sub)

		return bytes(result)

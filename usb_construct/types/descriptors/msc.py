# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#

from enum         import IntEnum

class MassStorageClassSpecificDescriptorTypes(IntEnum):
	PIPE_USAGE = 0x24

class MassStorageClassRequest(IntEnum):
	ADSC = 0x00
	''' Accept Device-Specific Command,'''
	GET_REQUESTS = 0xFC
	PUT_REQUESTS = 0xFD
	GET_MAX_LUN  = 0xFE
	BOMSR        = 0xFF
	''' Bulk-Only Mass Storage Reset '''

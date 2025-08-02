# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
#
# ⚠️ This was implemented off of a UAS-3 DRAFT ⚠️
# ⚠️ It may be incomplete or subtly wrong!     ⚠️

from enum         import IntEnum

import construct
from construct    import this

from ..descriptor import DescriptorField, DescriptorFormat, DescriptorNumber
from .msc         import MassStorageClassSpecificDescriptorTypes

class PipeID(IntEnum):
	COMMAND  = 0x01
	STATUS   = 0x02
	DATA_IN  = 0x03
	DATA_OUT = 0x04

class InformationUnitID(IntEnum):
	COMMAND         = 0x01
	SENSE           = 0x03
	RESPONSE        = 0x04
	TASK_MANAGEMENT = 0x05
	READ_READY      = 0x06
	WRITE_READY     = 0x07

class InformationUnitTaskAttribute(IntEnum):
	SIMPLE        = 0b000
	'''
	Specifies that the command be managed according to the rules for a simple task attribute (see SAM-6)
	'''
	HEAD_OF_QUEUE = 0b001
	'''
	Specifies that the command be managed according to the rules for a head of queue task attribute (see SAM-6)
	'''
	ORDERED       = 0b010
	'''
	Specifies that the command be managed according to the rules for an ordered task attribute (see SAM-6)
	'''
	ACA           = 0b100
	'''
	Specifies that the command be managed according to the rules for an automatic contingent allegiance task
	attribute (see SAM-6)
	'''

def command_priority(value: int) -> int:
	'''
	Converts an integer into a valid Command Priority that is ready to be or'd with
	an appropriate :py:class:`InformationUnitTaskAttribute`

	Parameters
	----------
	value: int
		The command priority as an integer.

	Returns
	-------
	int
		The truncated and shifted value.

	'''

	return (value & 0xF) << 3

class InformationUnitResponseCode(IntEnum):
	TASK_MANAGEMENT_FUNCTION_COMPLETE      = 0x00
	INVALID_INFORMATION_UNIT               = 0x02
	TASK_MANAGEMENT_FUNCTION_NOT_SUPPORTED = 0x04
	TASK_MANAGEMENT_FUNCTION_FAILED        = 0x05
	TASK_MANAGEMENT_FUNCTION_SUCCEEDED     = 0x08
	INCORRECT_LOGICAL_UNIT_NUMBER          = 0x09
	OVERLAPPED_TAG_ATTEMPTED               = 0x0A

class InformationUnitTaskManagementFunction(IntEnum):
	ABORT_TASK               = 0x01
	ABORT_TASK_SET           = 0x02
	CLEAR_TASK_SET           = 0x04
	LOGICAL_UNIT_RESET       = 0x08
	I_T_NEXUS_RESET          = 0x10
	CLEAR_ACA                = 0x40
	QUERY_TASK               = 0x80
	QUERY_TASK_SET           = 0x81
	QUERY_ASYNCHRONOUS_EVENT = 0x82


PipeUsageDescriptor = DescriptorFormat(
	'bLength'         / DescriptorNumber(4),
	'bDescriptorType' / DescriptorNumber(MassStorageClassSpecificDescriptorTypes.PIPE_USAGE),
	'bPipeID'         / DescriptorField('UAS Pipe Identifier'),
	'bReserved'       / DescriptorNumber(0)
)


CommandInformationUnit = DescriptorFormat(
	'bID'                 / DescriptorNumber(InformationUnitID.COMMAND),
	'bReserved0'          / DescriptorNumber(0),
	'wTag'                / DescriptorField('Interface Unit Tag'),
	'bmAttribute'         / DescriptorField(''),
	'bReserved1'          / DescriptorNumber(0),
	'CDBLen'              / construct.BitStruct(
		'Reserved' / construct.Const(0, construct.BitsInteger(2)),
		'Value'    / construct.BitsInteger(6),
	),
	'bReserved2'          / DescriptorNumber(0),
	'qwLogicalUnitNumber' / DescriptorField(''),
	'wCDB'                / DescriptorField(''),
	'CDBBytes'            / construct.Byte[this.CDBLen.Value * 4]
)

ReadReadyInformationUnit = DescriptorFormat(
	'bID'       / DescriptorNumber(InformationUnitID.READ_READY),
	'bReserved' / DescriptorNumber(0),
	'wTag'      / DescriptorField('')
)

WriteReadyInformationUnit = DescriptorFormat(
	'bID'       / DescriptorNumber(InformationUnitID.WRITE_READY),
	'bReserved' / DescriptorNumber(0),
	'wTag'      / DescriptorField('')
)

SenseInformationUnit = DescriptorFormat(
	'bID'              / DescriptorNumber(InformationUnitID.SENSE),
	'bReserved'        / DescriptorNumber(0),
	'wTag'             / DescriptorField(''),
	'wStatusQualifier' / DescriptorField(''),
	'qwReserved'       / DescriptorNumber(0),
	'wLength'          / DescriptorField(''),
	'SenseData'        / construct.Byte[this.wLength]
)

ResponseInformationUnit = DescriptorFormat(
	'bID'                             / DescriptorNumber(InformationUnitID.RESPONSE),
	'bReserved'                       / DescriptorNumber(0),
	'wTag'                            / DescriptorField(''),
	'qwAdditionalResponseInformation' / DescriptorField(''),
	'bResponseCode'                   / DescriptorField('')
)

TaskManagementInformationUnit = DescriptorFormat(
	'bID'                     / DescriptorNumber(InformationUnitID.TASK_MANAGEMENT),
	'bReserved0'              / DescriptorNumber(0),
	'wTag'                    / DescriptorField(''),
	'bTaskManagementFunction' / DescriptorField(''),
	'bReserved1'              / DescriptorNumber(0),
	'wTaskTag'                / DescriptorField(''),
	'qwLogicalUnitNumber'     / DescriptorField('')
)

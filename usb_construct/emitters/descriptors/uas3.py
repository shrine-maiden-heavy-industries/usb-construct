# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of usb-construct.
#
#
# ⚠️ This was implemented off of a UAS-3 DRAFT ⚠️
# ⚠️ It may be incomplete or subtly wrong!     ⚠️

from ...types.descriptors.uas3 import *
from ..                        import emitter_for_format

PipeUsageDescriptorEmitter = emitter_for_format(PipeUsageDescriptor)

#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2013, Daniel M. Lofaro
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */

import hubo_ach as ha
import ach
import sys
import time
import math
from ctypes import *
import dyno_include as di

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
d = ach.Channel(di.DYNO_REF_NAME)
s.flush()
r.flush()
d.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()
dyno = di.DYNO_REF()

print 'running'

while True:
	# Get the current feed-forward (state) 
	[statuss, framesizes] = d.get(dyno, wait=True, last=True)
	[statuss, framesizes] = r.get(ref, wait=False, last=True)

	if (dyno.uAR == 1):
		ref.ref[ha.LSP] = dyno.LSP
		ref.ref[ha.LSR] = dyno.LSR
		ref.ref[ha.LEB] = dyno.LEB

	if (dyno.uLG == 1):
		ref.ref[ha.RHR] = dyno.RHR
		ref.ref[ha.LHR] = dyno.LHR
		ref.ref[ha.RHP] = dyno.RHP 
		ref.ref[ha.LHP] = dyno.LHP
		ref.ref[ha.RKN] = dyno.RKN 
		ref.ref[ha.LKN] = dyno.LKN
		ref.ref[ha.RAP] = dyno.RAP 
		ref.ref[ha.LAP] = dyno.LAP
		ref.ref[ha.RAR] = dyno.RAR 
		ref.ref[ha.LAR] = dyno.LAR

	r.put(ref)
	time.sleep(.01)
	
# Close the connection to the channels
r.close()
s.close()
d.close()

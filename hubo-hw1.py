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
import state_include as si

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)

d = ach.Channel(di.DYNO_REF_NAME)
dyno = di.DYNO_REF()

a = ach.Channel(si.STATE_REF_NAME)
astate = si.STATE_REF()

a.flush()
#s.flush()
#r.flush()
#LSPstart = -1 * math.pi/2

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

armstate = 3 #initialize


# states 1 and 2 are the two arm waive motions, state 0 is no waive and arm down, state 1 is no wave and arm up
while True:
	[statuss, framesizes] = a.get(astate, wait=False, last=True)
	armstate = astate.ARM

	if 1==armstate:
		tstart = time.clock()	
		dyno.LEB = -2.85
		dyno.uAR = 1		
		d.put(dyno)
		astate.ARM = 2
		time.sleep(.5-(time.clock()-tstart))

	if 2==armstate:
		tstart = time.clock()
		dyno.LEB = -.25	
		dyno.uAR = 1	
		d.put(dyno)
		astate.ARM = 1
		time.sleep(.5-(time.clock()-tstart))

	if 0==armstate:
		tstart = time.clock()
		dyno.LSP = 0
		dyno.LSR = 0
		dyno.LEB = 0
		dyno.uAR = 1	
		d.put(dyno)
		time.sleep(.5-(time.clock()-tstart))
	
	if 3==armstate:
		dyno.LSP = -1 * math.pi/2
		dyno.LSR = 1.25
		dyno.LEB = -.75
		dyno.uAR = 1	
		d.put(dyno)	
		time.sleep(2)	

# Close the connection to the channels
r.close()
s.close()

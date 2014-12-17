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

#increased maxtorque of left ankle roll, left knee pitch left hip roll to 100

import hubo_ach as ha
import ach
import sys
import time
import math
from ctypes import *
import dyno_include as di
import state_include as si

d = ach.Channel(di.DYNO_REF_NAME)
dyno = di.DYNO_REF()

a = ach.Channel(si.STATE_REF_NAME)
astate = si.STATE_REF()

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
s.flush()
#r.flush()
a.flush()

#Set constants
#maxRAR = (math.pi/2)-1.415
maxRAR = .169
#maxRHR = -(math.pi/2)+1.415
maxRHR = -.169
#maxLAR = (math.pi/2)-1.415
maxLAR = .169
#maxLHR = -(math.pi/2)+1.415
maxLHR = -.169
startRKN = 1.0
startRHP = -.5
startRAP = -.5
startLKN = 1.0
startLHP = -.5
startLAP = -.5

steps = 5


def simSleep(tsim, Ts, state):
	time = tsim
	t = tsim + Ts	
	while(time < t):		
		[statuss, framesizes] = s.get(state, wait=False, last=False)
		time = state.time


# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

#get sim time
[statuss, framesizes] = s.get(state, wait=False, last=False)

#initialize arm to state 3 (raised no waiving)
astate.ARM = 3
a.put(astate)
time.sleep(2)

#set arm to state 1 (waiving)
astate.ARM = 1
a.put(astate)

#testcode
simSleep(state.time, 1, state)


#squat
[statuss, framesizes] = s.get(state, wait=False, last=False)
dyno.RKN = startRKN
dyno.LKN = startLKN
dyno.RHP = startRHP
dyno.LHP = startLHP
dyno.RAP = startRAP
dyno.LAP = startLAP
dyno.uLG = 1
d.put(dyno)
simSleep(state.time, .25, state)


#move cg to left
for x in range(0,steps):
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	dyno.RAR = state.joint[ha.RAR].pos + maxRAR/steps
	dyno.RHR = state.joint[ha.RHR].pos - maxRAR/steps
	dyno.LAR = state.joint[ha.LAR].pos + maxRAR/steps
	dyno.LHR = state.joint[ha.LHR].pos - maxRAR/steps
	dyno.uLG = 1
	d.put(dyno)
	simSleep(state.time, .5, state)

simSleep(state.time, .5, state)

#raise foot
for x in range(1,(steps+1)):
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	dyno.RKN = state.joint[ha.RKN].pos + 1.0/steps
	dyno.RHP = state.joint[ha.RHP].pos - .5/steps
	dyno.RAP = state.joint[ha.RAP].pos - .5/steps
	dyno.uLG = 1
	d.put(dyno)
	simSleep(state.time, .5, state)

#extend leg
for x in range(1,(steps+1)):
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	#[statuss, framesizes] = r.get(ref, wait=False, last=True)
	dyno.RKN = state.joint[ha.RKN].pos - 1.0/steps
	dyno.RAP = state.joint[ha.RAP].pos + 1.0/steps
	dyno.uLG = 1
	d.put(dyno)
	simSleep(state.time,.5,state)

#put foot down
dyno.LKN = 1.3
dyno.LHP = -.65
dyno.LAP = -.65
dyno.uLG = 1
d.put(dyno)
simSleep(state.time,.5,state)


#move cg to right from left
for x in range(1,steps*2):
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	dyno.LKN = state.joint[ha.LKN].pos - .5/(2*steps)
	dyno.LHP = state.joint[ha.LHP].pos - (-.5/(2*steps))
	dyno.RHP = state.joint[ha.RHP].pos - (-.4/(2*steps))
	dyno.RAP = state.joint[ha.RAP].pos - .4/(2*steps)
	dyno.RAR = state.joint[ha.RAR].pos - maxRAR/(2*steps)
	dyno.RHR = state.joint[ha.RHR].pos - maxRHR/(2*steps)
	dyno.LAR = state.joint[ha.LAR].pos - maxLAR/(2*steps)
	dyno.LHR = state.joint[ha.LHR].pos - maxLHR/(2*steps)
	dyno.uLG = 1
	d.put(dyno)
	simSleep(state.time, .5, state)

[statuss, framesizes] = s.get(state, wait=False, last=False)
dyno.RKN = 1.0
dyno.RHP = -.5
dyno.RAP = -.5
dyno.uLG = 1
d.put(dyno)

#Zero incase of drift
[statuss, framesizes] = r.get(ref, wait=False, last=True)
dyno.RAR = 0
dyno.RHR = 0
dyno.LAR = 0
dyno.LHR = 0
dyno.uLG = 1
d.put(dyno)

#move cg to right
for x in range(0,steps):
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	dyno.RAR = state.joint[ha.RAR].pos - (.01+maxRAR)/(steps)
	dyno.RHR = state.joint[ha.RHR].pos - (.01+maxRHR)/(steps)
	dyno.LAR = state.joint[ha.LAR].pos - (.01+maxLAR)/(steps)
	dyno.LHR = state.joint[ha.LHR].pos - (.01+maxLHR)/(steps)
	dyno.uLG = 1
	d.put(dyno)
	simSleep(state.time, 1, state)	

#lift left leg
for x in range(0, 2*steps):
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	dyno.LKN = state.joint[ha.LKN].pos + 1.0/(2*steps)
	dyno.LHP = state.joint[ha.LHP].pos - .5/(2*steps)
	dyno.LAP = state.joint[ha.LAP].pos - .5/(2*steps)
	dyno.uLG = 1
	d.put(dyno)
	simSleep(state.time, .5, state)

#step back even
[statuss, framesizes] = s.get(state, wait=False, last=False)
dyno.LHP = state.joint[ha.RHP].pos
dyno.LKN = state.joint[ha.RKN].pos
dyno.LAP = state.joint[ha.RAP].pos
dyno.LAR = state.joint[ha.RAR].pos
dyno.uLG = 1
d.put(dyno)

#sleep for the required 5 seconds
simSleep(state.time, 5, state)

#signal arm process to stop waiving
astate.ARM = 0
a.put(astate)

#stand up straight
dyno.RAR = 0
dyno.RHR = 0
dyno.LAR = 0
dyno.LHR = 0
dyno.uLG = 1
d.put(dyno)

# Close the connection to the channels
r.close()
s.close()
d.close()
a.close()

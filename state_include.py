#!/usr/bin/env python

from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16


STATE_REF_NAME =	'state-chan'

class STATE_REF(Structure):
    _pack_ = 1
    _fields_ = [("ARM",    c_double),
		("WALK",    c_double)]

#!/usr/bin/env python

from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16


DYNO_REF_NAME =	'dyno-ref-chan'

class DYNO_REF(Structure):
    _pack_ = 1
    _fields_ = [("uAR",    c_double),
		("uLG",    c_double),
		("LHR",    c_double),
		("LHP",	   c_double),
		("LKN",	   c_double),
		("LAP",	   c_double),
                ("LAR",    c_double),
                ("RHR",    c_double),
                ("RHP",    c_double),
                ("RKN",    c_double),
                ("RAP",    c_double),
                ("RAR",    c_double),
                ("LSP",    c_double),
                ("LEB",    c_double),
                ("LSR",    c_double) ]

from libc.stdio import *

cdef extern from "lsbatch.h":
    ctypedef long long int LS_LONG_INT
    ctypedef unsigned long long LS_UNS_LONG_INT

    ctypedef long time_t
    ctypedef unsigned short u_short

cdef extern from "lsf.h":
    extern enum valueType: LS_BOOLEAN, LS_NUMERIC, LS_STRING, LS_EXTERNAL
    extern enum orderType: INCR, DECR, NA

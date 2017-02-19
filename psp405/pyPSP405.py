#! /usr/bin/env python3   
#
#   Python module to control GW-Instek PSP-405 power supply units over a 
#   serial interface. This module is intended to be cross-platform (Linux, Windows).
# 
#   usage: ................... TODO ...................................... 
#
#   The power supply has 25 commands available. 
#   Every command is end up with <cr> (ASCII 0x0D OR ASCII 0x0D 0x0A acceptable).
#   The return message <cr> of the power supply is CR/LF (ASCII 0x0D 0x0A)
#
######################################################################################

import serial
import sys
import os
from .exceptions405 import NoPortParam, Permissions

class PSP405(object):
    def __init__ (self, port = None):
        '''
            PSP needs a serial connection interface
        '''
        if port == None:
            ## usage PSP405( <DEV_FILE/COM> )
            raise NoPortParam("usage: PSP405(port=<port>)")
        if 'ix' in os.name:
            if os.geteuid() != 0:
                ## On Linux root priviledges are needed for using /dev files
                raise Permissions("Root priviledges needed")
        # Create serial connection object and configure attributes
        self.ser            = serial.Serial()
        self.ser.port       = port
        self.ser.baudrate   = 2400
        self.ser.bytesize   = serial.EIGHTBITS 
        self.ser.parity     = serial.PARITY_NONE 
        self.ser.stopbits   = serial.STOPBITS_ONE 
        # TODO self.ser.timeout = 1            
        self.ser.xonxoff    = False     
        self.ser.rtscts     = False     
        self.ser.dsrdtr     = False    



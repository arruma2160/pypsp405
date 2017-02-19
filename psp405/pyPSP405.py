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

_commands = {
        'GET_STATUS_VALUES'   : 'L\r',
        'GET_OUTPUT_VOLT'     : 'V\r',
        'GET_OUTPUT_CURRENT'  : 'A\r',
        'GET_OUTPUT_LOAD'     : 'W\r',
        'GET_VOLT_LIMIT'      : 'U\r',
        'GET_CURRENT_LIMIT'   : 'I\r',
        'GET_LOAD_LIMIT'      : 'P\r',
        'GET_DEV_STATUS'      : 'F\r',
        'SET_VOLT_LIMIT'      : 'SUM\r',
        'SET_CUR_LIMIT'       : 'SIM\r',
        'SET_LOAD_LIMIT'      : 'SPM\r',
        # TODO implement rest command
}

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
    
    @property
    def status_values(self):
        pass

    @property
    def output_volt(self):
        pass
    @output_volt.setter
    def output_volt(self):
        pass

    @property
    def output_current(self):
        pass
    @output_current.setter
    def output_current(self):
        pass

    @property
    def output_load(self):
        pass
    @output_load.setter
    def output_load(self):
        pass

    @property
    def volt_limit(self):
        pass

    @property
    def current_limit(self):
        pass

    @property
    def load_limit(self):
        pass

    @property
    def dev_status(self):
        pass


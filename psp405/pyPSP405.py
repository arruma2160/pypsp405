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
import re
from .exceptions405 import NoPortParam, Permissions

_commands = {
        'GET_STATUS_VALUES'   : b'L\r',
        'GET_OUTPUT_VOLT'     : b'V\r',
        'GET_OUTPUT_CURRENT'  : b'A\r',
        'GET_OUTPUT_LOAD'     : b'W\r',
        'GET_VOLT_LIMIT'      : b'U\r',
        'GET_CURRENT_LIMIT'   : b'I\r',
        'GET_LOAD_LIMIT'      : b'P\r',
        'GET_DEV_STATUS'      : b'F\r',
        'SET_VOLT_LIMIT'      : b'SUM\r',
        'SET_CUR_LIMIT'       : b'SIM\r',
        'SET_LOAD_LIMIT'      : b'SPM\r',
        # TODO implement rest command
}

class PSP405(object):
    def __init__ (self, port = None, timeout = 2):
        '''
            PSP needs a serial connection interface
            use: 
                    psp = PSP405('/dev/ttyUSB0')
                    psp = PSP405('COM25')
                    psp = PSP405('COM25', 5)
                    psp = PSP405(timeout = 1, port = '/dev/ttyUSB0')
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
        self.ser.timeout    = timeout
        self.ser.xonxoff    = False     
        self.ser.rtscts     = False     
        self.ser.dsrdtr     = False    
    
    @property
    def status_values(self):
        self.ser.write(_commands['GET_STATUS_VALUES'])
        response = b''
        retry = 0   ## Allows retry in case in a first request to read() returns an empty string
        while not response.endswith(b'\r') and retry <= 3: # 3 retries allowed
            response = self.ser.read(100)
            retry += 1
        V, A, W, U, I, P, F = re.findall(r"\d*\.\d+|\d+", response.decode('utf-8'))
        return "V={};A={};W={};U={};I={};P={};F={}".format(V, A, W, U, I, P, F)

    @property
    def output_volt(self):
        self.ser.write(_commands['GET_OUTPUT_VOLT'])
    @output_volt.setter
    def output_volt(self, volt):
        self.ser.write(_commands['SET_VOLT_LIMIT'])

    @property
    def output_current(self):
        self.ser.write(_commands['GET_OUTPUT_CURRENT'])
    @output_current.setter
    def output_current(self, current):
        self.ser.write(_commands['SET_CUR_LIMIT'])

    @property
    def output_load(self):
        self.ser.write(_commands['GET_OUTPUT_LOAD'])
    @output_load.setter
    def output_load(self, load):
        self.ser.write(_commands['SET_LOAD_LIMIT'])

    @property
    def volt_limit(self):
        self.ser.write(_commands['GET_VOLT_LIMIT'])

    @property
    def current_limit(self):
        self.ser.write(_commands['GET_CURRENT_LIMIT'])

    @property
    def load_limit(self):
        self.ser.write(_commands['GET_LOAD_LIMIT'])

    @property
    def dev_status(self):
        self.ser.write(_commands['GET_DEV_STATUS'])


#! /usr/bin/env python3   
#

from unittest import TestCase, main
from mock import Mock,patch
from contextlib import contextmanager
from psp405 import PSP405, NoPortParam, Permissions
import os

@contextmanager
def mock_file(filepath,content=''):
    ''' 
        Creation of a temp file for testing purposes
    '''
    with open(filepath, 'w') as f:
        f.write(content)
    yield filepath
    try:
        os.remove(filepath)
    except Exception:
        pass


class TestSystemOnInitializerFailure(TestCase):
    ''' 
        Checking PSP405 class raises exceptions on misuse
    '''
    def test_verify_if_port_not_given_exception_raised(self):
        self.assertRaises(NoPortParam,PSP405)

    @patch('os.geteuid')
    def test_verify_if_linux_system_and_not_root_exception_raised(self, mock):
        mock.return_value = 1000 # Non-root user
        with mock_file(r'USB_MOCK'):             
            self.assertRaises(Permissions,PSP405,'USB_MOCK')


class TestPspSerialParameters(TestCase):
    ''' 
        Checking correct initialization of PSP405 class
        1) Passed device file (Linux) / COM (Windows)
        2) Root privileges (Linux)
        3) Serial connection parameters according PSP405 spec.
    '''
    @patch('os.geteuid')
    def test_parameters_serial_conn(self, mock):
        with mock_file(r'USB_MOCK'):             
            mock.return_value = 0   # Root 
            self.psp = PSP405('USB_MOCK')
            self.assertEqual(self.psp.ser.baudrate,2400)
            self.assertEqual(self.psp.ser.parity, 'N')
            self.assertEqual(self.psp.ser.bytesize, 8)
            self.assertEqual(self.psp.ser.stopbits, 1)
            self.assertEqual(self.psp.ser.xonxoff, False)
            self.assertEqual(self.psp.ser.rtscts, False)
            self.assertEqual(self.psp.ser.dsrdtr, False)


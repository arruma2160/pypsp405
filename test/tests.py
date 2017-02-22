#! /usr/bin/env python3   
#

from unittest import TestCase, main
from mock import Mock,patch
from contextlib import contextmanager
from psp405 import PSP405, NoPortParam, Permissions
import serial
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
        with mock_file('USB_MOCK'):             
            mock.return_value = 0   # Root 
            self.psp = PSP405('USB_MOCK')
            self.assertEqual(self.psp.ser.baudrate,2400)
            self.assertEqual(self.psp.ser.parity, 'N')
            self.assertEqual(self.psp.ser.bytesize, 8)
            self.assertEqual(self.psp.ser.stopbits, 1)
            self.assertEqual(self.psp.ser.xonxoff, False)
            self.assertEqual(self.psp.ser.rtscts, False)
            self.assertEqual(self.psp.ser.dsrdtr, False)


@patch('os.geteuid')
class TestRequestsCorrectness(TestCase):
    ''' 
    '''
    def test_request_status_values(self, mock):
        ''' Tests that we are able to retrieve 
            the correct answer at status request (twice)
        '''
        with mock_file('USB_MOCK'):             
            mock.return_value = 0   # Root 
            psp = PSP405('USB_MOCK')
            psp.ser = Mock(serial.Serial)
            psp.ser.read.return_value = b'V12.34A3.345W041.3U25I9.99P100F111111\r'
            response = psp.status_values
            psp.ser.write.assert_called_with(b'L\r')
            self.assertEqual(response, "V=12.34;A=3.345;W=041.3;U=25;I=9.99;P=100;F=111111")
            psp.ser.read.return_value = b'V11.34A4.345W043.3U25I9.99P100F111111\r'
            response = psp.status_values
            psp.ser.write.assert_called_with(b'L\r')
            self.assertEqual(response, "V=11.34;A=4.345;W=043.3;U=25;I=9.99;P=100;F=111111")


    def test_request_output_volt(self, mock):
        ''' Tests that we are able to retrieve 
            the correct answer at output_volt request (twice)
        '''
        with mock_file('USB_MOCK'):             
            mock.return_value = 0   # Root 
            psp = PSP405('USB_MOCK')
            psp.ser = Mock(serial.Serial)
            psp.ser.read.return_value = b'V012.45\r'
            response = psp.output_volt
            psp.ser.write.assert_called_with(b'V\r')
            self.assertEqual(response, "V=012.45")
            psp.ser.read.return_value = b'V011.21\r'
            response = psp.output_volt
            psp.ser.write.assert_called_with(b'V\r')
            self.assertEqual(response, "V=011.21")

    def test_request_output_current(self, mock):
        mock.return_value = 0   # Root 
        psp = PSP405('USB_MOCK')
        psp.ser = Mock(serial.Serial)
        psp.output_current
        psp.ser.write.assert_called_with(b'A\r')

    def test_request_output_load(self, mock):
        mock.return_value = 0   # Root 
        psp = PSP405('USB_MOCK')
        psp.ser = Mock(serial.Serial)
        psp.output_load
        psp.ser.write.assert_called_with(b'W\r')

    def test_request_volt_limit(self, mock):
        mock.return_value = 0   # Root 
        psp = PSP405('USB_MOCK')
        psp.ser = Mock(serial.Serial)
        psp.volt_limit
        psp.ser.write.assert_called_with(b'U\r')

    def test_request_current_limit(self, mock):
        mock.return_value = 0   # Root 
        psp = PSP405('USB_MOCK')
        psp.ser = Mock(serial.Serial)
        psp.current_limit
        psp.ser.write.assert_called_with(b'I\r')

    def test_request_load_limit(self, mock):
        mock.return_value = 0   # Root 
        psp = PSP405('USB_MOCK')
        psp.ser = Mock(serial.Serial)
        psp.load_limit
        psp.ser.write.assert_called_with(b'P\r')

    def test_request_dev_status(self, mock):
        mock.return_value = 0   # Root 
        psp = PSP405('USB_MOCK')
        psp.ser = Mock(serial.Serial)
        psp.dev_status
        psp.ser.write.assert_called_with(b'F\r')

    def test_request_set_volt_limit(self, mock):
        mock.return_value = 0   # Root 
        psp = PSP405('USB_MOCK')
        psp.ser = Mock(serial.Serial)
        psp.output_volt = 3
        psp.ser.write.assert_called_with(b'SUM\r')

    def test_request_set_cur_limit(self, mock):
        mock.return_value = 0   # Root 
        psp = PSP405('USB_MOCK')
        psp.ser = Mock(serial.Serial)
        psp.output_current = 5
        psp.ser.write.assert_called_with(b'SIM\r')

    def test_request_set_load_limit(self, mock):
        mock.return_value = 0   # Root 
        psp = PSP405('USB_MOCK')
        psp.ser = Mock(serial.Serial)
        psp.output_load = 3
        psp.ser.write.assert_called_with(b'SPM\r')


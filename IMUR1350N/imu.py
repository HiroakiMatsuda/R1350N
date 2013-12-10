#!/usr/bin/env python
#coding:utf-8
# ver. 1.31210
# This module has been tested on python ver.2.6.6
# pySerial(http://pyserial.sourceforge.net/) is need to use.
# Please see the manual for how to use each of the methods and procedures.
# (C) 2013 Matsuda Hiroaki

import serial
import time
import cmath

class R1350N():

    def __init__(self):
        self.myserial = serial.Serial()
        print('Generated the serial object')
        
    def open_port(self, port, baudrate, timeout = 1):
        self.myserial.port = port
        self.myserial.baudrate = baudrate
        self.myserial.timeout = timeout
        self.myserial.parity = serial.PARITY_NONE
        try:
            self.myserial.open()
        except IOError:
            print('Failed to open port, check the device and port number')
        else:
            print('Succeede to open port: ' + port)

    def close_port(self):
        self.myserial.close()
    
    def initialize(self, length):
        self.myserial.flushOutput()
        #self.myserial.flushInput()
        self.myserial.write('$MIB,RESET*87')
        time.sleep(1)
        receive = self.myserial.read(length)

        return receive

        
    def cue_data(self):
        while 1:
            head = [ord(self.myserial.read(1))]
            
            if head[0] == 0xAA:
                head.append(ord(self.myserial.read(1)))
                
                if head[1] == 0x00:
                    receive = self.myserial.read(13)
                    data = [ord(temp) for temp in receive]
                    
                    data = head + data

                    return self._convert_data(data)

    def read_data(self):
        receive = self.myserial.read(15)

        if len(receive) != 15:
            return self.cue_data()
        
        data = [ord(temp) for temp in receive]

        return self._convert_data(data)

    def _convert_data(self, data):
        check_sum = 0
        for temp in data[2:14]:
            check_sum += temp
        check_sum &= 0xFF

        if check_sum == data[14]:
            index = data[2]
            angle = (( data[4]  << 8) & 0xFF00) | (data[3]  & 0xFF)
            rate  = (( data[6]  << 8) & 0xFF00) | (data[5]  & 0xFF)
            x_acc = (( data[8]  << 8) & 0xFF00) | (data[7]  & 0xFF)
            y_acc = (( data[10] << 8) & 0xFF00) | (data[9]  & 0xFF)
            z_acc = (( data[12] << 8) & 0xFF00) | (data[11] & 0xFF)

            if angle > 32767:
                angle = -((angle - 1) ^ 0xFFFF)
            if rate > 327674:
                rate = -((rate - 1) ^ 0xFFFF)
            if x_acc > 32767:
                x_acc = -((x_acc - 1) ^ 0xFFFF)
            if y_acc > 32767:
                y_acc = -((y_acc - 1) ^ 0xFFFF)
            if z_acc > 32767:
                z_acc = -((z_acc - 1) ^ 0xFFFF)

            return index, angle / 100.0, angle * cmath.pi /18000.0, rate / 100.0, x_acc / 1000.0, y_acc / 1000.0, z_acc / 1000.0

    def _write_command(self, send):
        self.myserial.flushOutput()
        self.myserial.flushInput()
        self.myserial.write("".join(map(chr, send)))

                
if __name__ == '__main__':
    import imu
    myimu = imu.R1350N()
    myimu.open_port('/dev/ttyUSB0', 115200)

    while len(myimu.initialize(82)) != 82:
              myimu.initialize(82)
    for i in xrange(1000):
	print myimu.cue_data()
        
    myimu.close_port()

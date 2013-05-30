'''
Created on May 23, 2013

@author: me
'''

import serial
import binascii
from ConfigParser import SafeConfigParser

class Dlf(object):
    '''
    DLF class: connect and setup device.
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def DLF_Get_Att_Val (self, val):
        '''
        Convert attribute value.
        '''
        nval = int(round((31.5 - val)/0.5, 0))
        if nval < 0:
            return '%02X' % 0
        else:
            return '%02X' % nval

    def DLF_Set_Defaults(self):
        '''
        Testing serial communication
        '''
        
        parser = SafeConfigParser()
        parser.read('configs/dlf.ini')
        
        ser = serial.Serial()
        ser.baudrate = parser.getint('Connect', 'serial_baudrate')
        ser.port = parser.get('Connect', 'serial_port')
        print 'status:\> sending data over serial:', ser.port
        ser.open()

        for section_name in ['DefaultsChng', 'DefaultsCnst']:
            for name, value in parser.items(section_name):
                buff = parser.get('ATT_Def', name).split(',')
                value = int(value)
                #print name, '=', value,
                data = "%s%s%s" % (buff[0], self.DLF_Get_Att_Val(value/2), '0D')
                #print data,
                ser.write(binascii.unhexlify(data))
                data = "%s%s%s" % (buff[1], self.DLF_Get_Att_Val(value-(value/2)), '0D')
                #print data
                ser.write(binascii.unhexlify(data))
        #print "400D"
        ser.write(binascii.unhexlify("400D")) 
        ser.close()
        
    def DLF_Set_Up(self):
        '''
        Testing serial communication
        '''
        
        parser = SafeConfigParser()
        parser.read('configs/dlf.ini')
        
        ser = serial.Serial()
        ser.baudrate = parser.getint('Connect', 'serial_baudrate')
        ser.port = parser.get('Connect', 'serial_port')
        print 'status:\> sending data over serial:', ser.port
        ser.open()

        for section_name in ['DefaultsComp']:
            for name, value in parser.items(section_name):
                buff = parser.get('ATT_Def', name + value).split(',')
                buff = ''.join(buff)
                print name, '=', value, '->', buff
                data = binascii.unhexlify(buff)
                ser.write(data)
                ser.write(data)
                ser.write(binascii.unhexlify('400D'))
        ser.close()

if __name__ == "__main__":
    
    data = Dlf()
    data.DLF_Set_Up()
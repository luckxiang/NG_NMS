'''
Created on May 23, 2013

@author: me
'''

import serial
import binascii
from ConfigParser import SafeConfigParser

class DlfSerial(object):
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
        ser = serial.Serial()
        ser.baudrate = 19200
        ser.port = "COM1"
        print ser
        ser.open()
        print 'status:\> serial open status:', ser.isOpen()
        
        parser = SafeConfigParser()
        parser.read('../configs/dlf.ini')

        for section_name in ['DefaultsChng', 'DefaultsCnst']:
            for name, value in parser.items(section_name):
                buff = parser.get('ATT_Def', name).split(',')
                value = int(value)
                data = "%s%s%s" % (buff[0], self.DLF_Get_Att_Val(value/2), '0D')
                #print data
                ser.write(binascii.unhexlify(data))
                data = "%s%s%s" % (buff[1], self.DLF_Get_Att_Val(value-(value/2)), '0D')
                #print data
                ser.write(binascii.unhexlify(data))
        ser.write(binascii.unhexlify("400D")) 
        ser.close()
        print 'status:\> done!'

# import binascii
# import socket
# import struct
# import sys
# #CreateaTCP/IPsocket
# sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address=('localhost',10000)
# sock.connect(server_address)
# values=(1,'ab',2.7)
# packer=struct.Struct('I2sf')
# packed_data=packer.pack(*values)
# print 'values=',values
# try:
#     #Senddata
#     print>>sys.stderr,'sending %r'%binascii.hexlify(packed_data)
#     sock.sendall(packed_data)
# finally:
#     print>>sys.stderr,'closing socket'
# sock.close()

if __name__ == "__main__":
    
    data = DlfSerial()
    data.DLF_Set_Defaults()
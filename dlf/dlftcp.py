'''
Created on May 29, 2013

@author: VitalieG
'''

import binascii
from ConfigParser import SafeConfigParser
import socket
import sys

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
        
        server_address=('192.168.140.76', 1001)
        parser = SafeConfigParser()
        parser.read('../configs/dlf.ini')

        data = ''
        for section_name in ['DefaultsChng', 'DefaultsCnst']:
            for name, value in parser.items(section_name):
                print name, value
                buff = parser.get('ATT_Def', name).split(',')
                value = int(value)
                data1 = "%s%s%s" % (buff[0], self.DLF_Get_Att_Val(value/2), '0D')
                data2 = "%s%s%s" % (buff[1], self.DLF_Get_Att_Val(value-(value/2)), '0D')
                data = ''.join((data, data1))
                data = ''.join((data, data2))
        data = ''.join((data, '400D'))
        data = binascii.unhexlify(data)

        #CreateaTCP/IPsocket
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        
        try:
            # Sending data
            print >> sys.stderr,'hex: %r' % binascii.hexlify(data)
            print >> sys.stderr,'bin: %r' % data
            sock.sendall(data)
        finally:
            print >> sys.stderr,'status:\> done! -> closing socket'
        sock.close()

    def DLF_Set_Up(self):
        '''
        Testing serial communication
        '''
        
        server_address=('192.168.140.76', 1001)
        parser = SafeConfigParser()
        parser.read('../configs/dlf.ini')

        data = ''
        temp = []
        for section_name in ['DefaultsComp']:
            for name, value in parser.items(section_name):
                print name, '=', value
                buff = parser.get('ATT_Def', name + value).split(',')
                buff = ''.join(buff)
                temp.append(buff)
        temp = ''.join(temp)
        data = binascii.unhexlify(temp)

        #CreateaTCP/IPsocket
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        
        try:
            # Sending data
            print >> sys.stderr,'hex: %r' % binascii.hexlify(data)
            print >> sys.stderr,'bin: %r' % data
            sock.sendall(data)
            sock.sendall(data)
        finally:
            print >> sys.stderr,'status:\> done! -> closing socket'
        sock.close()

if __name__ == "__main__":
    
    data = Dlf()
    data.DLF_Set_Up()

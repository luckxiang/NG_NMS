'''
Created on Mar 6, 2013

@author: me
'''

import telnetlib

class Grab:
    '''
    To grab VSAT statistics over telnet session.
    '''
    
    # store telnet session.
    tn = None

    def __init__(self, ip, port, timeout):
        '''
        Constructor: Initialize ip, port, timeout
        '''
        self.ip = ip
        self.port = port
        self.timeout = timeout
        
    def connect(self):
        '''
        Connect to VSAT over telnet with ip, port, timeout.
        '''
        self.tn = telnetlib.Telnet(self.ip, self.port, self.timeout)
        return self.tn
    
    def disconnect(self):
        '''
        Disconnect from VSAT.
        '''
        self.tn.close()
  
    def grab(self, command, stop_pattern):
        '''
        Get statistics over telnet with command until stop_pattern.
        '''
        print "Telnet:\nIP: %s\nPORT %s\nCOMMAND: %s\nSTOP: %s\n" % (self.ip, self.port, command, stop_pattern)
       
        try:
            tn = self.connect()
        except Exception as e:
            print "%s" % e

        tn.write(command + "\r\n")
        output = tn.read_until(stop_pattern, self.timeout)
        
        self.disconnect()
        return output
    
    def check_bb(self):
        '''
        Check if bb status is up.
        '''
        import re
        
        command = 'bb links'
        stop_pattern = 'sec)'
        
        output = self.grab(command, stop_pattern)
        try:
            rez = re.search("Total Backbone Links UP = 0.", output)
            if rez:
                return False
            else:
                return True

        except Exception as e:
            print "BB seems to be down?\nError: - %s" % e
        
        
        
        
        
        
        
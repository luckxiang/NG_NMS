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
        Constructor: Initialize ip, port
        '''
        self.ip = ip
        self.port = port
        self.timeout = timeout
        
    def connect(self):
        '''
        Connect to VSAT over telnet with ip, port, timeout.
        '''
        try:
            self.tn = telnetlib.Telnet(self.ip, self.port, self.timeout)
        except Exception as e:
            print e
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
       
        tn = self.connect()

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
            print "BB down?\nError: - %s" % e
            
    def ftp_selftest(self, ftptype, duration):
        '''
        Start ftp selftest.
        '''
        try:
            if ftptype == 'inbound':
                command = 'ip selftest ftpup 1 %s' % duration
            elif ftptype == 'outbound':
                command = 'ip selftest ftpdown %s' % duration
        except Exception as e:
            print e
        
        stop_pattern = '>'
        tn = self.connect()
        tn.write(command + "\r\n")
        tn.read_until(stop_pattern, self.timeout)
                
        self.disconnect()
        
    def get_stats(self):
        '''
        Get VSAT output statistics.
        '''
        try:
            if self.check_bb():
                command = 'bb stat'
                stop_pattern = '''END Statistics for BB link'''
                bb_stat = self.grab(command, stop_pattern)
                print "%s" % bb_stat
                command = 'bb link'
                stop_pattern = '''*********** End BB Link'''
                bb_link = self.grab(command, stop_pattern)
                print "%s" % bb_link
                # return bb_stat and bb_link
                return "%s\r\n%s" % (bb_stat, bb_link)
        except Exception as e:
            print "%s" % e
        
        
        
        
        
        
        
        
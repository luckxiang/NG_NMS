'''
Created on Mar 6, 2013

@author: me
'''
#import getpass
import telnetlib

class Grab:
    '''
    TODO: classdocs: Telnet class related info
    '''


    def __init__(self, ip, port, timeout):
        '''
        Constructor: Initialize IP and PORT
        '''
        self.ip = ip
        self.port = port
        self.timeout = timeout
  
    def grab(self, command):
        '''
        Get statistics over telnet protocol with pycurl
        '''
        
        print "TODO: Get from VSAT SELFTEST statistics using:\nIP: %s\nPORT %s\nCommand: %s\n" % (self.ip, self.port, command)
        
        #user = raw_input("Enter your remote account: ")
        #password = getpass.getpass()
        
        tn = telnetlib.Telnet(self.ip, self.port, self.timeout)
        
        #tn.read_until("login: ")
        #tn.write(user + "\n")
        #if password:
        #    tn.read_until("Password: ")
        #    tn.write(password + "\n")
        
        tn.write(command + "\r\n")
     
        print tn.read_until('quit', self.timeout)
'''
Created on Mar 6, 2013

@author: me
'''
import pycurl

class Telnet():
    '''
    TODO: classdocs: Telnet class related info
    '''


    def __init__(self, IP, PORT):
        '''
        Constructor: Initialize IP and PORT
        '''
        self.IP = IP
        self.PORT = PORT
        
    ## Callback function invoked when body data is ready
    def body(self,command):
        # Print body data to stdout
        import sys
        sys.stdout.write(command)
        # Returning None implies that all bytes were written
    
    def grab(self, command, VERBOSE = False):
        '''
        Get statistics over telnet protocol with pycurl
        '''
        
        import cStringIO
        buf = cStringIO.StringIO()
        
        print "TODO: Get from VSAT SELFTEST statistics using:\nIP: %s\nPORT %s\nCommand: %s\n" % (self.IP, self.PORT, command)
        
        HOST = {'IP':self.IP, 'PORT':self.PORT}
        
        stats = pycurl.Curl()
        stats.setopt(pycurl.URL, "telnet://%(IP)s:%(PORT)s" % HOST)
        #stats.setopt(pycurl.TIMEOUT, 5)
        stats.setopt(pycurl.VERBOSE, VERBOSE)
        #stats.setopt(pycurl.QUOTE, ["%s" % command])
        
        try:
            stats.perform()
            stats.setopt(pycurl.WRITEFUNCTION, buf.write)
        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: %s %s' % (errno, errstr)
                    
        print "OUTPUT: %s" % buf.getvalue()
        output = buf.getvalue()
        buf.close()
        stats.close()
        return output
    
        
    
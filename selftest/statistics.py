'''
Created on Mar 6, 2013

@author: me
'''

import telnetlib
import logging
import re

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
            return self.tn 
        except Exception as e:
            logging.exception('TELNET:')
            print e
    
    def disconnect(self):
        '''
        Disconnect from VSAT.
        '''
        self.tn.close()
  
    def grab(self, command, stop_pattern):
        '''
        Get statistics over telnet with command until stop_pattern.
        '''
        try:       
            tn = self.connect()
    
            tn.write(command + "\r\n")
            output = tn.read_until(stop_pattern, self.timeout)
            
            self.disconnect()
            return output
        except Exception as e:
            logging.exception('GRAB:')
            print e
    
    def check_bb(self):
        '''
        Check if bb status is up.
        '''
        try:
            command = 'bb links'
            stop_pattern = 'sec)'
            
            output = self.grab(command, stop_pattern)
            rez = re.search("Total Backbone Links UP = 0.", output)
            if rez:
                return False
            else:
                return True
        except Exception as e:
            logging.exception('BB STATUS:')
            print e
            
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
                output = {}
                command = 'bb link'
                stop_pattern = '''*********** End BB Link'''
                bb_link = self.grab(command, stop_pattern)
                for line in bb_link.split('\n'):
                    if not line.strip():
                        continue
                    iotraffic = re.match(r'^Current:.*$', line.strip('\r\n'))
                    if iotraffic:
                        iotraffic = iotraffic.group(0)
                        ib_bit_rate, ob_bit_rate = iotraffic.split('.')[0:2]
                        output['max_ib_bit_rate'] = re.search(r'\d+', ib_bit_rate).group(0) 
                        output['max_ob_bit_rate'] = re.search(r'\d+', ob_bit_rate).group(0)

                command = 'bb stat'
                stop_pattern = '''END Statistics for BB link'''
                bb_stat = self.grab(command, stop_pattern)
                for line in bb_stat.split('\n'):
                    if not line.strip():
                        continue
                    worlds = line.strip('\r\n')
                    worlds = worlds.split()
                    if worlds[0] == 'RETRANSMITTED':
                        output['nr_of_retrans_ob_pckts'] = worlds[1].lstrip('0')
                        output['nr_of_retrans_ib_pckts'] = worlds[2].lstrip('0')
                
                command = 'rsp cpu get statistics'
                stop_pattern = '''>'''
                cpu_stats = self.grab(command, stop_pattern)
                for line in cpu_stats.split('\n'):
                    if not line.strip():
                        continue
                    cpu_load = re.match(r'^CPU utilization.*$', line.strip('\r\n'))
                    if cpu_load:
                        cpu_load = cpu_load.group(0)
                        cpu_value = re.search(r'\$\d+\$', cpu_load)
                        output['cpu_load'] = cpu_value.group(0)
                
                return output
        except Exception as e:
            print "%s" % e
        
        
        
        
        
        
        
        
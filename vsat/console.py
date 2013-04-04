'''
Created on Mar 6, 2013

@author: me
'''

import telnetlib
import re
import sys
import time

class Grab:
    '''
    Get VSAT statistics over telnet session.
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
            print e
            print
            print 'VSAT: ip: {0} port:{1}'.format(self.ip, self.port)
            print 'HINT: ngnmstest.py --check vsat --name <vsat_name>'
            sys.exit()
    
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
            print e
    
    def check_bb(self):
        '''
        Check if bb status is up.
        '''
        try:
            command = 'bb up'
            stop_pattern = '>'
            self.grab(command, stop_pattern)
            time.sleep(3)
            command = 'bb links'
            stop_pattern = 'sec)'
            
            output = self.grab(command, stop_pattern)
            print
            print 'step:\> Checking link status!'
            link_status = False
            for line in output.split('\r'):
                if 'UP' in line.split():
                    link_status = line.strip().rstrip('.')
                    print 'status:',link_status
                    # return link_status and bb link message.
                    return (int(link_status.split()[5]), link_status)
            # return link_status and bb link message.
            return (link_status, output)
        except Exception as e:
            print e

    def ftp_selftest(self, ftptype, duration):
        '''
        Start ftp selftest.
        '''
        # resetting cpu stats.
        command = 'rsp cpu get statistics 1'
        stop_pattern = '''>'''
        self.grab(command, stop_pattern)
        time.sleep(3)
        
        if ftptype == 'inbound':
            command = 'ip selftest ftpup 1 %s' % duration
        elif ftptype == 'outbound':
            command = 'ip selftest ftpdown %s' % duration

        stop_pattern = '>'
        tn = self.connect()
        print
        print "test:\> %s" % command
        tn.write('\r\n')
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
                        output['Max IB bit rate'] = int(re.search(r'\d+', ib_bit_rate).group(0)) 
                        output['Max OB bit rate'] = int(re.search(r'\d+', ob_bit_rate).group(0))

                command = 'bb stat'
                stop_pattern = '''END Statistics for BB link'''
                bb_stat = self.grab(command, stop_pattern)
                for line in bb_stat.split('\n'):
                    if not line.strip():
                        continue
                    words = line.strip('\r\n')
                    words = words.split()
                    if words[0] == 'RETRANSMITTED':
                        output['Number of OB retransmit packets'] = words[1].lstrip('0') or 0
                        output['Number of IB retransmit packets'] = words[2].lstrip('0') or 0
                    if words[0] == 'UNNUMBERED':
                        output['Number of transmitted OB packets'] = words[1].lstrip('0') or 0
                        output['Number of received IB packets'] = words[2].lstrip('0') or 0
                        
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
                        output['VSAT CPU'] = cpu_value.group(0)
                
                return output
        except Exception as e:
            print "%s" % e

if __name__ == '__main__':
    '''
    Main program.
    '''
    pass

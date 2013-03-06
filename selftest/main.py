'''
Created on Mar 6, 2013

@author: me
'''
'''
Automated Testing flow:

1.     Using REST API we export the configuration file {JSON format with OID}.
2.     From our Excel file with Test Cases we read one line that contains Test Case To Run.
3.     Changing the value of needed OID with needed values.
4.     Using REST API, we import configuration file to NGNMS.
5.     Checking NGNMS is ready for statistics result.
6.     Starting SELFTEST Mode.
7.     Over telnet protocol, we collect result data.
8.     Storing data into Excel file.
9.     Go to again to P.1 until go through all Test Cases.
'''

# TODO: Read configuration files
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('../confs/test.cfg')

# Device Uder Test: dut_ip, dut_port
dut_ip = config.get('vsat', 'ip')
dut_port = config.get('vsat', 'port')
grab_command = config.get('command', 'rsp_cpu_get_statistics')
timeout = 2


# TODO: Using REST API - exporting the configuration {JSON format with OID}.
#

# TODO: Read Test Cases from Excel file line by line
#

# TODO: Change the value of needed OID with new values.
#

# TODO: Using REST API - import configuration file to NGNMS
# 

# TODO: Checking if NGNMS load new configuration files and ready to start SELFTEST.
#

# TODO: Starting SELFTEST mode.
# 

# TODO: Get statistics over telnet protocol from devices: VSATs.
#
def getStats(grab_command):
    from grabstats import Grab
    
    stats = Grab(dut_ip, dut_port, timeout)
    stats.grab(grab_command)


# TODO: Storing data into Excel file.
#

# TODO: Test Task.
#

if __name__ == '__main__':
    
    
    # Grab statistics from VSAT.
    getStats(grab_command)
    

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
device_under_test_ip = config.get('vsat', 'ip')
device_under_test_port = config.get('vsat', 'port')
command = config.get('command', 'bb_links')
stop_pattern = 'sec)'
timeout = 20

from statistics import Grab
vsat = Grab(device_under_test_ip, device_under_test_port, timeout)

# TODO: Using REST API - exporting the configuration {JSON format with OID}.
# TODO: Read Test Cases from Excel file line by line
# TODO: Change the value of needed OID with new values.
# TODO: Using REST API - import configuration file to NGNMS
# TODO: Checking if NGNMS load new configuration files and ready to start SELFTEST.
# TODO: Starting SELFTEST mode.
# TODO: Get statistics over telnet protocol from devices: VSATs.
# TODO: Storing data into Excel file.
# TODO: Test Task.


if __name__ == '__main__':

    try:
        if vsat.check_bb():
            bb_stat = vsat.grab(command = 'bb stat', stop_pattern = '''END Statistics for BB link to CPA 11''')
            bb_link = vsat.grab(command = 'bb link', stop_pattern = '''*********** End BB Link to CPA 11 Status info *****************''')
            
            print "%s" % bb_stat
            print "%s" % bb_link
    except Exception as e:
        print "%s" % e

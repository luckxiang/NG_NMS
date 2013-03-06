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
7.     Over Telnet protocol, we collect result data.
8.     Storing data into Excel file.
9.     Go to again to P.1 until go through all Test Cases.
'''

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
from telnet import Telnet 

# grab output with command
tn = Telnet("127.0.0.1", 23)
tn.grab('whoami', VERBOSE = True)



# TODO: Storing data into Excel file.
#

# TODO: Test Task.
#

if __name__ == '__main__':
    pass
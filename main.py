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
config.read('./confs/test.cfg')

# Device Uder Test
device_under_test_ip = config.get('vsat', 'ip')
device_under_test_port = config.get('vsat', 'port')
command = config.get('command', 'bb_links')
stop_pattern = 'sec)'
timeout = 20

from selftest import statistics
vsat = statistics.Grab(device_under_test_ip, device_under_test_port, timeout)

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
    
    import time   
    
    # TODO: put this value in excel config file.
    number_of_tries = 10

    with open("./data/some.csv") as f:
        for line in f:
            next(f)
            for param in line.split(',')[1:12]:
                # TODO: set working environment
                print param,
            # TODO: check bb status
            counter = 0
            while True:
                if counter == number_of_tries:
                    print "Exceeded number of tries per test case!"
                    break
                if vsat.check_bb():
                    # TODO: start selftest
                    duration = line.split(',')[12]
                    for ftptype in ['inbound', 'outbound']:
                        vsat.ftp_selftest(ftptype, duration)
                        time.sleep(duration/2)
                        # TODO: grab output
                        output = vsat.get_stats()
                        # TODO: save data
                        time.sleep((duration/2) + 10)
                    break
                counter = counter + 1
                time.sleep(10)

        print "Success!"

        


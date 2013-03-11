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

# Device under test: ip, port, timeout, number_of_tries
# TODO: put this value in excel config file.
from testcases import excel2csv
data = excel2csv.Excel('./data/test1.xlsx')
data.export_sheet_to_csv('CONFIGS', './configs/vsat.csv')
data.export_sheet_to_csv('TESTCASES', './data/testcases.csv')

configs = data.read_configs('./configs/vsat.csv')
device_under_test_ip = configs.get('VSAT IP')
device_under_test_port = configs.get('VSAT PORT')
timeout = configs.get('TIMEOUT')
number_of_tries = configs.get('NUMBER OF TRIES')

print "%s %s %s %s" % (device_under_test_ip, device_under_test_port, timeout, number_of_tries)

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
    
    pass
    
    import time   
 
    with open("./data/some.csv") as f:
        for line in f:
            print line
            for param in line.split(',')[1:12]:
                # TODO: set working environment
                print param,
            # Checking bb status before starting SELFTEST
            counter = 0
            while True:
                if counter == number_of_tries:
                    print "Exceeded number of tries per test case!"
                    break
                if vsat.check_bb():
                    duration = line.split(',')[12]
                    for ftptype in ['inbound', 'outbound']:
                        vsat.ftp_selftest(ftptype, duration)
                        time.sleep(duration/2)
                        # TODO: grab statistics from output
                        output = vsat.get_stats()  
                        print output                      
                        # TODO: save data to csv file.
                        time.sleep((duration/2) + 10)
                    break
                counter = counter + 1
                time.sleep(10)


        


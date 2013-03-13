'''
Created on Mar 6, 2013

@author: me
'''
from string import upper
import time 
import sys

'''
Automated Testing flow:

1.    Using REST API - set working point NGNMS.
2.    Check working point before start SELFTEST.
3.    Starting SELFTEST Mode.
4.    Over telnet protocol, we collect result data.
5.    Storing data into Excel file.
6.    Go to again to P.1 until go through all Test Cases.
'''

def testcases(xlfile):
    '''
    Parse file with testcases and return all needed data.
    '''
    from xlparser import excel
    data = excel.Parser(xlfile)
    testcases = data.get_testcases()
    # return test cases and HUB, VSAT connection parameters
    return testcases

# TODO: do multiple vsat testing.
from vsat import console
vsat = console.Vsat("192.168.140.76", 1016, 20)

def show_time_counter(time_interval):
    '''
    Show time counter.
    '''
    for second in xrange(1,time_interval+1):
        print "\tCounter: ",
        print '{0}\r'.format(second),
        time.sleep(1)
    print

def main():
    '''
    Main program.
    '''
    with open("./data/some_3_cases.csv") as f:
        for line in f:
            print "======="*10
            print " "*25,"TESTCASE: %s" % line.split(',')[0]
            print "======="*10
            print "\nTest:\>",
            for param in line.split(',')[0:12]:
                # TODO: set working environment
                print param,
            print
            # Checking bb status before starting SELFTEST
            counter = 0
            while True:
                if counter == number_of_tries:
                    print "Exceeded number of tries per test case!"
                    sys.exit(0)
                if vsat.check_bb():
                    duration = line.split(',')[11]
                    duration = int(duration)
                    print "VSAT bb links status: UP!\n"
                    wait_bb_links_to_finish = 5
                    show_time_counter(wait_bb_links_to_finish)
                    
                    for ftptype in ['inbound', 'outbound']:
                        print
                        print "-"*25, 'TEST:',line.split(',')[0],upper(ftptype), "-"*25
                        print "\nStarting selftest for %s with duration %d seconds!" % (upper(ftptype), duration)
                        vsat.ftp_selftest(ftptype, duration)
                        first_time_half = duration/2
                        print "Waiting %d seconds before getting statistics! ...\n\n" % first_time_half, 
                        show_time_counter(int(first_time_half))
                        print "\nNext, getting statistics from VSAT!\n"
                        output = vsat.get_stats()
                        for key in sorted(output.keys()):
                            print key,' = ',output[key]                      
                        # TODO: save data to csv file.
                        # TODO: fix last test case wait time!
                        next_time_half = duration/2
                        print "\nWaiting %d seconds to finish %s selftest!\n" % (next_time_half, upper(ftptype))
                        show_time_counter(int(next_time_half))
                    print
                    break
                print "\nVSAT bb links status: DOWN!\n"
                counter = counter + 1
                print "Counter: %d Number of tries: %d" % (counter, number_of_tries)
                show_time_counter(try_again_timeout)

# TODO: Using REST API - set working point NGNMS.
# TOOD: Check working point before start SELFTEST.
# TODO: Storing data into Excel file.

if __name__ == '__main__':
    '''
    Run main program.
    '''
    main()
    
  
  



        


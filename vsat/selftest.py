'''
Created on Mar 6, 2013

@author: me
'''
import time
from string import upper

class Selftest:
    '''
    Run selftest mode for VSAT.
    '''
    def __init__(self,xlfile):
        '''
        Get excel file.
        '''
        self.xlfile = xlfile
        
    def get_testcases(self):
        '''
        Parse file with testcases and return all needed data.
        '''
        from xlparser import excel
        data = excel.Parser(self.xlfile)
        testcases = data.get_testcases()
        # return test cases and HUB, VSAT connection parameters
        return testcases
    
    def show_time_counter(self, time_interval):
        '''
        Show time counter.
        '''
        for second in xrange(1,time_interval+1):
            print "\tCounter: ",
            print '{0}\r'.format(second),
            time.sleep(1)
        print
        


# TODO: Using REST API - set working point NGNMS.
# TOOD: Check working point before start SELFTEST.
# TODO: Storing data into Excel file.

if __name__ == '__main__':
    '''
    Run main program.
    '''
    vsat = Selftest('../data/test.xls');
    testcases = vsat.get_testcases()
    
    for sheet in sorted(testcases.keys()):
        if sheet == 'headers':
            continue
        print "X"*65
        print " "*22, 'SHEET:',sheet
        print "X"*65
        for row in testcases[sheet].keys():
            if row == 0:
                continue
            print
            print "-"*20, 'SHEET %s ROW:' % upper(sheet), row, "-"*20
            for cell in testcases['headers'][sheet]:
                print ' '*5,'{0:35} = {1:35}'.format(str(cell), str(testcases[sheet][row][cell]))
        print
        
    
    
    
    
  
  



        


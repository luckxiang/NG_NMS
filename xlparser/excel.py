'''
Created on Mar 9, 2013

@author: me
'''

import os
import sys

class Parser:
    '''
    Export excel and export to csv format.
    '''
    excel = None
    extention = None
    logger = False

    def __init__(self, xlfile):
            '''
            Parsing xls and xlsx files.
            '''
            self.xlfile = xlfile
            # check if file exist.
            try:
                with open(self.xlfile): pass
            except Exception as e:
                print
                print '*'*60
                print e
                print '*'*60
                sys.exit()
            
            # check file extention.
            excell_type = os.path.basename(xlfile)
            self.extention = excell_type.split('.')[1]
            if self.extention == 'xls':
                from xlparser import ioxls
                self.excel = ioxls.Xls(self.xlfile)
            else:
                print
                print '*'*60
                print "Unrecongnized file extention!"
                print "File: %s" % xlfile
                print '*'*60
                sys.exit()

    def get_testcases(self):
        '''
        Get all info from excel file.
        '''
        print "="*60
        print "\tINFO: Excel file %s!" % (self.xlfile)
        print "="*60
        testcases = self.excel.get_testcases()
        
        # display all test cases
        if self.logger:
            self.excel.display(testcases)
        print

        # return all data from excel file.
        return testcases

    def display(self, testcases, state = None, sheet = None):
        '''
        Display sheets content.
        '''
        self.excel.display(testcases, state, sheet)

if __name__ == "__main__":
    '''
    Main program.
    '''
    data = Parser('../data/demo.xls')
    data.logger = True
    data.get_testcases()

    data = Parser('../data/test.xls')
    data.logger = True
    data.get_testcases()

    data = Parser('../data/test.xlsx')
    data.logger = True
    data.get_testcases()
    
    
    
    
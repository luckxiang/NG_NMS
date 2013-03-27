'''
Created on Mar 9, 2013

@author: me
'''

import os
import string
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
                with open(xlfile): pass
            except Exception as e:
                print e
                sys.exit()
            
            # check file extention.
            excell_type = os.path.basename(xlfile)
            self.extention = excell_type.split('.')[1]
            if self.extention == 'xls':
                from xlparser import ioxls
                self.excel = ioxls.Xls(self.xlfile)
            else:
                print "Unrecongnized file extention!"
                print "File: %s" % xlfile
                sys.exit()

    def get_testcases(self):
        '''
        Get all info from excel file.
        '''
        print "="*70
        print "\tINFO: Excel file %s!" % (self.xlfile)
        print "="*70
        testcases = self.excel.get_testcases()
        
        # print testcases
        if self.logger:
            self.excel.display(testcases)
        print
        # return all data from excel file.
        return testcases

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
    
    
    
    
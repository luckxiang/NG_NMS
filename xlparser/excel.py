'''
Created on Mar 9, 2013

@author: me
'''

import os
import string

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

            excell_type = os.path.basename(xlfile)
            self.extention = excell_type.split('.')[1]
            if self.extention == 'xls':
                from xlparser import ioxls
                self.excel = ioxls.Xls(self.xlfile)
            elif self.extention == 'xlsx':
                from xlparser import ioxlsx
                self.excel = ioxlsx.Xlsx(self.xlfile)

    def get_testcases(self):
        '''
        Get all info from excel file.
        '''
        print "="*70
        print "\tINFO: Excel file %s with %s extention" % (self.xlfile, string.upper(self.extention))
        print "="*70
        testcases = self.excel.get_testcases()
        
        # print testcases
        if self.logger:
            self.excel.display(testcases)
        print
        # return all data from excel file.
        return testcases

if __name__ == "__main__":
    
    data = Parser('../data/test.xls')
    data.logger = True
    data.get_testcases()
    
    del data
    data = Parser('../data/test.xlsx')
    data.logger = True
    data.get_testcases()
    
    
    
    
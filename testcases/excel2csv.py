'''
Created on Mar 9, 2013

@author: me
'''

import os

class Excel(object):
    '''
    Export excel and export to csv format.
    '''
    excell = None

    def __init__(self, xlfile):
            '''
            Constructor
            '''
            self.xlfile = xlfile

            excell_type = os.path.basename(xlfile)
            extention = excell_type.split('.')[1]
            if extention == 'xls':
                from testcases import ioxls
                self.excell = ioxls.Xls(self.xlfile)
            elif extention == 'xlsx':
                from testcases import ioxlsx
                self.excell = ioxlsx.Xlsx(self.xlfile)

    def export_sheet_to_csv(self, sheetname, csvfile):
        '''
        Export excel sheet to csv file.
        '''
        self.excell.export_sheet_to_csv(sheetname, csvfile)
                    
    def read_configs(self, csvfile):
        '''
        Read configs from csv file.
        '''
        with open(csvfile) as f:
            configs = {}
            for line in f:
                key, value = line.split(',')
                configs[key] = value.rstrip('\n')
            return configs
        
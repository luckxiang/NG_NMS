'''
Created on Mar 9, 2013

@author: me
'''

import os

class Parser:
    '''
    Export excel and export to csv format.
    '''
    excel = None

    def __init__(self, xlfile):
            '''
            Constructor
            '''
            self.xlfile = xlfile

            excell_type = os.path.basename(xlfile)
            extention = excell_type.split('.')[1]
            if extention == 'xls':
                from xlparser import ioxls
                self.excel = ioxls.Xls(self.xlfile)
            elif extention == 'xlsx':
                from xlparser import ioxlsx
                self.excel = ioxlsx.Xlsx(self.xlfile)

    def export_sheet_to_csv(self, sheetname, csvfile):
        '''
        Export excel sheet to csv file.
        '''
        self.excel.export_sheet_to_csv(sheetname, csvfile)
                    
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
        
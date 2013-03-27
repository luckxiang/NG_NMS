'''
Created on Mar 6, 2013

@author: me
'''

import time

class Selftest:
    '''
    Run selftest mode for VSAT.
    '''
    
    data = None
    
    def __init__(self,xlfile):
        '''
        Get excel file.
        '''
        self.xlfile = xlfile
        from xlparser import excel
        self.data = excel.Parser(self.xlfile)
        
    def get_testcases(self):
        '''
        Get all info from excel file
        '''
        return self.data.get_testcases()
    
    def display(self, testcases, state = None, sheet = None):
        '''
        Display info from excel file.
        '''
        self.data.display(testcases, state, sheet);

    def save_to_excel(self, result):
        '''
        Save result to excel file.
        '''
        print "Saving result to excel file!"
        
        from xlrd import open_workbook
        from xlutils.copy import copy
        from xlwt import easyxf
        
        rb = open_workbook(self.xlfile, formatting_info=1, on_demand=True)
        wb = copy(rb)
        sheet = 'D-TESTCASES'
        styleOk = easyxf('font: name Times New Roman;'
               'borders: left thin, right thick, top thin, bottom thin;'
               'pattern: pattern solid, fore_colour light_green;'
               'alignment: horiz center, vert center')
        styleFail = easyxf('font: name Times New Roman;'
               'borders: left thin, right thick, top thin, bottom thin;'
               'pattern: pattern solid, fore_colour rose;'
               'alignment: horiz center, vert center')
        for row in result[sheet].keys():
            for cell in result['headers'][sheet][10:]:
                wb.get_sheet(3).write(row, result['headers'][sheet].index(cell), result[sheet][row][cell], styleOk)

        wb.save('data/output.xls')
        print "DONE!"

def show_time_counter(time_interval):
    '''
    Show time counter.
    '''
    for second in xrange(1,time_interval+1):
        print "\tCounter: ",
        print '{0}\r'.format(second),
        time.sleep(1)
    print


def show(xlfile,state=None, sheet=None):
    '''
    Show all testcases.
    '''
    vsat = Selftest(xlfile);
    testcases = vsat.get_testcases()
    vsat.display(testcases, state, sheet)


if __name__ == '__main__':
    '''
    Run main program.
    '''
    pass
    

'''
Created on Mar 6, 2013

@author: me
'''

import time
from vsat import console
from string import upper

class Selftest:
    '''
    Run selftest mode for VSAT.
    '''
    
    data = None
    number_of_tries = 3
    tries_timeout = 2
    
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
    
    def display(self, testcases, state = None, sheet = None, name = None):
        '''
        Display info from excel file.
        '''
        self.data.display(testcases, state, sheet, name);

    def check(self, state = None, device = None, vsatname = None):
        '''
        Check device availability.
        '''
        if device == 'vsat': self.vsat_status(state, vsatname)

        
    def vsat_status(self, state = None, vsatname = None):
        '''
        Check vsat.
        '''
        testcases = self.data.get_testcases()
        header, states, cases = testcases

        if state == None:
            state = 'enabled'

        sheet = 'VSAT'
        vsats = states[state][sheet]
        header = header[sheet][0]
        print 'H'*60
        print upper(state).rjust(30)
        print 'H'*60
        for host in vsats:
            vsat = vsats[host]
            if vsatname != None and vsatname != vsat[1]:
                print '{0:5}: {1:10}'.format(sheet, vsat[1])
                continue
            print '-'*50
            print "-- %s : %s --".rjust(30) % (vsat[1], upper(state))
            print '-'*50
            for key, value in zip(header, vsats[host]):
                print "{0:20} = {1:20}".format(key, str(value))
            ip = vsat[header.index('Console IP')]
            port = int(vsat[header.index('Console PORT')])
            connection_timeout = int(vsat[header.index('Connection timeout')])
            number_of_tries = self.number_of_tries
            tries_timeout = self.tries_timeout
 
            # checking vsats.
            session = console.Grab(ip, port, connection_timeout)
            for next_step in xrange(1,number_of_tries + 1):
                print
                print "Checking connection ..."
                connected = session.connect()
                if connected:
                    print "-> SUCCESS!"
                    print
                    break
                else:
                    print "Attempt number: %s" % next_step
                    print "-> FAILED!"
                    print
                if next_step != number_of_tries:
                    print "Retrying to connect in %s sec ..." % tries_timeout
                    self.show_time_counter(tries_timeout)
            print '-'*60

    def show_time_counter(self, time_interval):
        '''
        Show time counter.
        '''
        for second in xrange(1,time_interval+1):
            print "\tCounter: ",
            print '{0}\r'.format(second),
            time.sleep(1)
        print

    def save_to_excel(self, testcases, state = None, name = None):
        '''
        Save result to excel file.
        '''
        print "Saving result to excel file!"
        
        header, states = testcases
        
        if state == None:
            states_keys = states.keys()
        else:
            states_keys = [state]
        # force just for test cases sheet.
        sheet = 'TESTCASES'

        from xlrd import open_workbook
        from xlutils.copy import copy
        from xlwt import easyxf
        
        rb = open_workbook(self.xlfile, formatting_info=1, on_demand=True)
        wb = copy(rb)
        
        styleOk = easyxf('font: name Times New Roman;'
               'borders: left thin, right thick, top thin, bottom thin;'
               'pattern: pattern solid, fore_colour light_green;'
               'alignment: horiz center, vert center')
        styleFail = easyxf('font: name Times New Roman;'
               'borders: left thin, right thick, top thin, bottom thin;'
               'pattern: pattern solid, fore_colour rose;'
               'alignment: horiz center, vert center')
        for state in states_keys:
            for row in states[state][sheet].keys():
                for cell in header[sheet][0][33:]:
                    wb.get_sheet_by_name(sheet).write(row, states[state][sheet].index(cell), states[state][sheet][row][cell], styleOk)
        try:
            wb.save('data/output.xls')
        except Exception as e:
            print e
        
        print
        print '-'*60
        print
        print "\t\tGood job!\n\t\tCongratulations! @};-\n\t\tWell done!\n"
        print
        print '-'*60

def show(xlfile, state=None, sheet=None, name = None):
    '''
    Display all, vsat, hub, testcases with enabled or disabled state.
    '''
    ngnms = Selftest(xlfile);
    testcases = ngnms.get_testcases()
    ngnms.display(testcases, state, sheet, name)

def check(xlfile, state = None, device = None, name = None):
    '''
    Check device availability.
    '''
    ngnms = Selftest(xlfile)
    ngnms.check(state, device, name)
    
def run(xlfile, state = None, name = None):
    '''
    Run testcase(s}.
    '''
    print 'Todo: run testcase: ', state, name

if __name__ == '__main__':
    '''
    Run main program.
    '''
    xlfile = '../data/demo.xls'
    data = Selftest(xlfile)
    testcases = data.get_testcases()
    header, states, cases = testcases
    for state in cases.keys():
        for sheet in cases[state].keys():
            for row in cases[state][sheet].keys():
                for cell in cases[state][sheet][row]:
                    print cell,cases[state][sheet][row][cell]
                print
            
        
            
    pass
    

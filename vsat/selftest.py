'''
Created on Mar 6, 2013

@author: me
'''

import time
from string import upper
from vsat import vconsole as console

# time for one step in stdout print.
page_time_step = 0.35

class Selftest:
    '''
    Run selftest mode for VSAT.
    '''
    
    testcases = None
    
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
        self.testcases = data.get_testcases()
        # return test cases and HUB, VSAT connection parameters
        return self.testcases
    
    def display(self):
        '''
        Display all info in excel file.
        '''
        for sheet in sorted(self.testcases.keys()):
            if sheet == 'headers':
                continue
            print "X"*65
            print " "*22, 'SHEET:',sheet
            print "X"*65
            for row in self.testcases[sheet].keys():
                if row == 0:
                    continue
                print
                print "-"*20, 'SHEET %s ROW:' % upper(sheet), row, "-"*20
                # print slowly.
                time.sleep(page_time_step)
                for cell in self.testcases['headers'][sheet]:
                    print ' '*5,'{0:35} = {1:35}'.format(str(cell), str(self.testcases[sheet][row][cell]))
            print
            
    def show_active_testcases(self):
        '''
        Create only enabled rows and summary.
        '''
        enabled_testcases = {}
        for sheet in sorted(self.testcases.keys()):
            enabled_testcases[sheet] = {}
            if sheet == 'headers':
                enabled_testcases[sheet] = self.testcases[sheet]
                continue
            print "H"*65
            print " "*22, 'SHEET:',sheet
            print "H"*65
            print
            enabled_rows = 0
            disabled_rows = 0
            for row in self.testcases[sheet].keys():
                if row == 0:
                    continue
                enabled_testcases[sheet][row] = {}
                if ('Active' in self.testcases[sheet][row].keys() and  
                    upper(str(self.testcases[sheet][row].get('Active'))) != 'X'):
                    disabled_rows += 1
                    continue
                else:
                    enabled_rows += 1
                    enabled_testcases[sheet][row] = self.testcases[sheet][row]
                print
                print "-"*20, 'SHEET %s ROW:' % upper(sheet), row, "-"*20
                time.sleep(page_time_step)
                for cell in self.testcases['headers'][sheet]:
                    print ' '*5,'{0:35} = {1:35}'.format(str(cell), str(self.testcases[sheet][row][cell]))
            print
            print '*'*34
            print upper('%s summary:' % sheet)
            print ' '*5, "{0:20} = {1:20}".format('Enabled rows:', str(enabled_rows))
            print ' '*5, "{0:20} = {1:20}".format('Disabled rows:', str(disabled_rows))
            print ' '*5, "{0:20} = {1:20}".format('Total rows:', str(enabled_rows + disabled_rows))
            print '*'*34
            print
        # return enabled rows only.
        # return enabled_testcases

    def get_active_testcases(self):
        '''
        Get active testcases.
        '''
        enabled_testcases = {}
        for sheet in sorted(self.testcases.keys()):
            if sheet == 'headers':
                # get all sheets headers.
                enabled_testcases[sheet] = self.testcases[sheet]
                continue
            enabled_testcases[sheet] = {}
            for row in self.testcases[sheet].keys():
                if row == 0:
                    continue
                if ('Active' in self.testcases[sheet][row].keys() and upper(str(self.testcases[sheet][row].get('Active'))) == 'X'):
                    enabled_testcases[sheet][row] = self.testcases[sheet][row]
                    
        # return active testcases only.
        return enabled_testcases



    def check_availability(self):
        '''
        Check VSAT's availability.
        '''
        for sheet in self.testcases.keys():
            if sheet == 'C-VSAT':
                vsat = self.testcases[sheet]
                print "*"*60
                print " "*10,"Checking connection to VSAT's:"
                print "*"*60
                vsats_status = {}
                vsats_status['SUCCESS!'] = {}
                vsats_status['FAILED!'] = {}
                for host in vsat.keys():
                    if host == 0 or vsat[host].get('Active') != 'X':
                        continue
                    VSAT_NAME = vsat[host].get('Name')
                    VSAT_ID = int(vsat[host].get('ID'))
                    IP = vsat[host].get('Console IP')
                    PORT = int(vsat[host].get('Console PORT'))
                    CONNECTION_TIMEOUT = int(vsat[host].get('Connection timeout'))
                    NUMBER_OF_TRIES = int(vsat[host].get('Number of tries'))
                    TRIES_TIMEOUT = int(vsat[host].get('Tries timeout'))
                    
                    print "%s ID:%s ip:%s port:%s TIMEOUT:%s" % (VSAT_NAME, VSAT_ID, IP, PORT, CONNECTION_TIMEOUT)
                    session = console.Grab(IP, PORT, CONNECTION_TIMEOUT)
                    time.sleep(page_time_step)
                    for next_step in xrange(1,NUMBER_OF_TRIES + 1):
                        print "Checking connection ..."
                        connected = session.connect()
                        if connected:
                            vsats_status['SUCCESS!'][host] = vsat[host]
                            print "-> SUCCESS!"
                            print
                            break
                        else:
                            vsats_status['FAILED!'][host] = vsat[host]
                            print "Attempt number: %s" % next_step
                            print "-> FAILED!"
                            print
                        if next_step != NUMBER_OF_TRIES:
                            print "Retrying to connect in %s sec ..." % TRIES_TIMEOUT
                            show_time_counter(TRIES_TIMEOUT)
                print
                print "*"*60
                print " "*10, "VSATs Summary:"
                print "*"*60
                for status in ['SUCCESS!', 'FAILED!']:
                    for vsat in vsats_status[status].keys():
                        name = vsats_status[status][vsat].get('Name')
                        vsat_id = int(vsats_status[status][vsat].get('ID'))
                        ip = vsats_status[status][vsat].get('Console IP')
                        port = int(vsats_status[status][vsat].get('Console PORT'))
                        print "Name:{0:8} id:{1:5} ip:{2:18} port:{3:5} <<->> {4:10}".format(name, str(vsat_id), ip, str(port), status)
        # return vsats_status hash 
        # with success and failed vsats.
        return vsats_status
    
    def run_active_testcases(self):
        '''
        Run active testcases.
        '''

        active_testcases = self.get_active_testcases()
        
        number_of_tries = 2
        
        for sheet in sorted(active_testcases.keys()):
            if sheet == 'headers' or not active_testcases[sheet]:
                continue
            print
            print "X"*65
            print " "*22, 'SHEET:',sheet
            print "X"*65
            print
            for row in sorted(active_testcases[sheet].keys()):
                print "-"*20, 'SHEET %s ROW:' % upper(sheet), row, "-"*20
                # print slowly.
                time.sleep(page_time_step)
                # Checking bb status before starting SELFTEST
                if sheet == 'D-TESTCASES':
                    counter = 0
                    while True:
                        if counter == number_of_tries:
                            print "Exceeded number of tries per test case!"
                            break
                        from vsat import vconsole
                        vsat = vconsole.Grab('192.168.140.76', 1016, 10)
                        connected = vsat.connect()
                        if connected and vsat.check_bb():
                            duration = int(active_testcases[sheet][row].get('Test duration'))
                            for ftptype in ['inbound', 'outbound']:
                                vsat.ftp_selftest(ftptype, duration)
                                time.sleep(duration/2)
                                output = vsat.get_stats() 
                                if ftptype == 'inbound':
                                    nr_of_retransmited_ib_pckts = output['Number of IB retransmit packets']
                                    nr_of_transmited_ib_pckts = output['Number of transmitted OB packets']
                                    max_ob_bit_rate = output['Max IB bit rate']
                                else:
                                    output['Number of IB retransmit packets'] = nr_of_retransmited_ib_pckts
                                    output['Number of transmitted IB packets'] = nr_of_transmited_ib_pckts
                                    output['Max IB bit rate'] = max_ob_bit_rate
                                time.sleep((duration/2) + 2)
                            break
                        counter = counter + 1
                for cell in active_testcases['headers'][sheet]:
                    if sheet == 'D-TESTCASES' and cell in active_testcases['headers'][sheet][10:]:
                        active_testcases[sheet][row][cell] = output.get(cell)
                    print ' '*5,'{0:35} = {1:35}'.format(str(cell), str(active_testcases[sheet][row][cell]))
                print
        # return active test cases results.
        return active_testcases

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
        style0 = easyxf('font: name Times New Roman;'
               'borders: left thin, right thick, top thin, bottom thin;'
               'pattern: pattern solid, fore_colour light_green;'
               'alignment: horiz center, vert center')
        style1 = easyxf('font: name Times New Roman;'
               'borders: left thin, right thick, top thin, bottom thin;'
               'pattern: pattern solid, fore_colour rose;'
               'alignment: horiz center, vert center')
        for row in result[sheet].keys():
            for cell in result['headers'][sheet][10:]:
                wb.get_sheet(3).write(row, result['headers'][sheet].index(cell), result[sheet][row][cell], style0)

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


def show_all_testcases(xlfile):
    '''
    Show all testcases.
    '''
    vsat = Selftest(xlfile);
    vsat.get_testcases()
    vsat.display()

def show_active_testcases(xlfile):
    '''
    Show only active testcases.
    '''
    vsat = Selftest(xlfile);
    vsat.get_testcases()
    vsat.show_active_testcases()

def run_active_testcases(xlfile):
    '''
    Run testcases.
    '''
    vsat = Selftest(xlfile);
    vsat.get_testcases()
    # get result.
    result = vsat.run_active_testcases()
    # save result to excel file.
    vsat.save_to_excel(result)

def show_vsat_testcases(xlfile):
    '''
    Show and check vsats testcases.
    '''
    vsat = Selftest(xlfile);
    vsat.get_testcases()
    vsat.check_availability()

    
if __name__ == '__main__':
    '''
    Run main program.
    '''
    pass
    
    
        
    
    
    
    
  
  



        


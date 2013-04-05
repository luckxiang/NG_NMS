'''
Created on Mar 6, 2013

@author: me
'''

import time
from vsat import console
from string import upper
from ngnms import biaspoint

output_xlfile = 'data/output.xls'
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
    
    def display(self, testcases, sheet = None, name = None,  *state):
        '''
        Display info from excel file.
        '''
        self.data.display(testcases, sheet, name, *state);

    def check(self, state = None, device = None, vsatname = None):
        '''
        Check device availability.
        '''
        if device == 'vsat': self.vsat_status(state, vsatname)
        if device == 'hub': self.check_ngnms()

    def check_ngnms(self):
        '''
        Check ngnms hub status.
        '''
        data = Selftest(self.xlfile)
        testcases = data.get_testcases()
        header, states, cases = testcases
        # getting first active network segment..
        ngnms_info = {}
        for hub in cases['enabled']['HUB'].keys():
            if cases['enabled']['HUB'][hub].get('Active') != '':
                ngnms_info = cases['enabled']['HUB'][hub]
            break
        ngnms = biaspoint.Ngnms(**ngnms_info)
        ngnms.check_ngnms()
        
        
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
        link_status = False
        print 'H'*60
        print upper(state).rjust(30)
        print 'H'*60
        for host in vsats:
            vsat = vsats[host]
            if vsatname != None and vsatname != vsat[1]:
                print '{0:5}: {1:10}'.format(sheet, vsat[1])
                continue
            print '-'*60
            print "-- %s : %s --".rjust(30) % (vsat[1], upper(state))
            print '-'*60
            for key, value in zip(header, vsats[host]):
                print "{0:20} = {1:20}".format(key, str(value))
            ip = vsat[header.index('Console IP')]
            port = int(vsat[header.index('Console PORT')])
            connection_timeout = int(vsat[header.index('Connection timeout')])
            number_of_tries = int(vsat[header.index('Number of tries')])
            tries_timeout = int(vsat[header.index('Tries timeout')])
 
            # checking vsats.
            session = console.Grab(ip, port, connection_timeout)
            for next_step in xrange(1,number_of_tries + 1):
                print
                print "step:\> Checking connection ..."
                print "status:",
                connected = session.connect()
                if connected:
                    print "-> SUCCESS!"
                    link_status, message = session.check_bb()
                    if link_status:
                        print 'status: ->Link UP!'
                    else:
                        print 'status: ->Link DOWN!'
                    break
                else:
                    print "status: Attempt number: %s" % next_step,
                    print "-> FAILED!"
                if next_step != number_of_tries:
                    print
                    self.show_time_counter(tries_timeout)
            print '-'*60
        return link_status

    def show_time_counter(self, time_interval):
        '''
        Show time counter.
        '''
        for second in xrange(1,time_interval+1):
            print 'step:\> Please wait {0} sec: [{1}]\r'.format(time_interval, second),
            time.sleep(1)
        print

    def run(self, testcases, state = None, name = None):
        '''
        Running test.
        '''
        header, states, cases = testcases
        number_of_tries = 2
        # force just TESTCASES sheet.
        sheet = 'TESTCASES'
        # Status change to True when exist data to save.
        status = False
        if state == None:
            states_keys = states.keys()
        else:
            states_keys = state

        # getting ngnms first active hub info.
        ngnms_info = {}
        for hub in cases['enabled']['HUB'].keys():
            if cases['enabled']['HUB'][hub].get('Active') != '':
                ngnms_info = cases['enabled']['HUB'][hub]
            break

        # show ngnms network tree.
        self.check(state = None, device = 'hub', vsatname = None)

        # getting first active VSAT.
        for vsat in cases['enabled']['VSAT'].keys():
            if states['enabled']['VSAT'][vsat][0] != '':
                vsat_data = cases['enabled']['VSAT'][vsat]
                vsat_ip = vsat_data.get('Console IP')
                vsat_port = int(vsat_data.get('Console PORT'))
                vsat_timeout = int(vsat_data.get('Connection timeout'))
                tries_timeout = int(vsat_data.get('Tries timeout'))
                number_of_tries = int(vsat_data.get('Number of tries'))
                vsatname = vsat_data.get('Name')
            break

        # Checking VSAT, cicle if vsat bb link is down.
        while not self.vsat_status(None, vsatname):
            # waiting time is tries_timeout.
            print 'status: waitting vsat link up ...'
            self.show_time_counter(tries_timeout)
        
        result_data = {}
        for state in states_keys:
            print 'H'*60
            print upper(state).rjust(30)
            print 'H'*60
            print
            
            result_data[state] = {}
            for row in sorted(states[state][sheet]):
                current_case = states[state][sheet][row][1]

                # adjusting selecting test case.
                if sheet == 'TESTCASES': 
                    current_case = int(current_case)
                if name != None and '%s' % name != '%s' % current_case:
                    print '{0}: {1}'.format(sheet, current_case)
                    continue
                else:
                    print
                    print '-'*60
                    print ' '*20, '{0}: {1}'.format(sheet, current_case)
                    print '-'*60
                    print

                # setting ngnms working point
                testcase = cases[state][sheet][row]
                ngnms = biaspoint.Ngnms(**ngnms_info)
                ngnms.set_ngnms_working_point(testcase)

                for nextstep in xrange(1,number_of_tries + 1):
                    print 'status: waitting vsat link up ...'
                    self.show_time_counter(tries_timeout)

                    print 'info:\> connecting to ... ip:{0} port:{1} timeout:{2}'.format(vsat_ip, vsat_port, vsat_timeout)
                    vsat = console.Grab(vsat_ip, vsat_port, vsat_timeout)
                    # changing 'rsp param set param 34' <ob_symbol_rate>
                    command = 'rsp param set param 34 %s' % testcase.get('OB symbol rate')
                    stop_pattern = '>'
                    print 'info:\> %s' % command
                    vsat.grab(command, stop_pattern)
 
                    # wait ...
                    self.show_time_counter(5)
                     
                    # rebooting vsat..
                    command = 'rsp board reset board'
                    print 'info:\> %s' % command
                    stop_pattern = '>'
                    vsat.grab(command, stop_pattern)
                    
                    connected = vsat.connect()
                    link_status, message = vsat.check_bb()
                    if connected and link_status:
                        duration = int(cases[state][sheet][row].get('Test duration'))
                        for ftptype in ['inbound', 'outbound']:
                            vsat.ftp_selftest(ftptype, duration)
                            print 'step:\> %s -> start!' % ftptype
                            self.show_time_counter(duration/2)
                            output = vsat.get_stats()
                            if ftptype == 'inbound':
                                nr_of_retransmited_ib_pckts = output['Number of IB retransmit packets']
                                nr_of_transmited_ib_pckts = output['Number of transmitted OB packets']
                                max_ob_bit_rate = output['Max IB bit rate']
                                cpu_ib = output.get('VSAT CPU')
                            else:
                                output['Number of IB retransmit packets'] = nr_of_retransmited_ib_pckts
                                output['Number of transmitted OB packets'] = nr_of_transmited_ib_pckts
                                output['Max IB bit rate'] = max_ob_bit_rate
                                output['VSAT CPU'] = '[%s]/[%s]' % (cpu_ib.strip('$'), output.get('VSAT CPU').strip('$'))
                            print 'status: %s -> done!' % ftptype
                            if ftptype != 'outbound': self.show_time_counter((duration/2) + 2)
                        break
                    else:
                        print 'ERROR: VSAT not OK!'
                        self.show_time_counter(tries_timeout)
                else:
                    print "info:\> Exceeded [%s] number of tries per test case!" % number_of_tries
                    continue
                print
                print '-'*25,'TEST: %s' % current_case, '-'*24
                result_data[state][row] = cases[state][sheet][row]
                for key in header[sheet][0]:
                    # print step to screen.
                    time.sleep(0.1)
                    if key in output.keys():
                        cases[state][sheet][row][key] = output[key]
                    if key == 'Max OB bit rate':
                        print
                        print '-'*25,'OUTPUT: %s' % current_case, '-'*24
                        print
                    print '{0:38} = {1:30}'.format(key, str(cases[state][sheet][row][key]))
                    # Check if we have data to save
                    status = True
                print
                print '-'*60
                print

        # saving data to file
        if status:
            print
            print "info:\> Saving result to [%s] excel file!" % output_xlfile
            print 
            self.save_row_to_excel(header[sheet][0], result_data)

    def save_row_to_excel(self, header, output):
        '''
        Save result to excel file.
        '''
        from xlrd import open_workbook
        from xlutils.copy import copy
        from xlwt import easyxf

        rb = open_workbook(self.xlfile, formatting_info=1, on_demand=True)
        wb = copy(rb)
        styleEnabled = easyxf('font: name Times New Roman;'
               'borders: left thin, right thick, top thin, bottom thin;'
               'pattern: pattern solid, fore_colour light_green;'
               'alignment: horiz center, vert center')
        styleDisabled = easyxf('font: name Times New Roman;'
               'borders: left thin, right thick, top thin, bottom thin;'
               'pattern: pattern solid, fore_colour pale_blue;'
               'alignment: horiz center, vert center')
        for state in output.keys():
            # Set row style.
            if state == 'enabled':
                style = styleEnabled
            elif state == 'disabled':
                style = styleDisabled
            for row in output[state].keys():
                for cell in header[32:]:
                        wb.get_sheet(1).write(row, header.index(cell), output[state][row].get(cell), style)

        # Check if file is closed.
        while True:
                try:
                    wb.save(output_xlfile)
                except Exception as e:
                    print e
                    # file already exists, try again
                    print
                    print 'Please close file first [%s], then continue: ' % output_xlfile,
                    raw_input('-> [ENTER]')
                    continue
                print
                print 'H'*60
                print '\nSUCCESS!: Successfully saved data to file: [%s]!\n' % output_xlfile
                print 'H'*60
                break

        # Success! We are the beast from the beasts,
        # In the blackest than blackest and deeper source code forest! 
        # NOTE: Joke! :p /* I just finished this project */
        print
        print '-'*60
        print "\n\t\tGood job!\n\t\tCongratulations! @};-\n\t\tWell done!\n"
        print '-'*60

def show(xlfile, sheet=None, name = None, *state):
    '''
    Display all, vsat, hub, testcases with enabled or disabled state.
    '''
    ngnms = Selftest(xlfile);
    testcases = ngnms.get_testcases()
    ngnms.display(testcases, sheet, name, *state)

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
    ngnms = Selftest(xlfile)
    testcases = ngnms.get_testcases()
    ngnms.run(testcases, state, name)

if __name__ == '__main__':
    '''
    Run main program.
    '''
    xlfile = '../data/demo.xls'
    data = Selftest(xlfile)
    testcases = data.get_testcases()
    state = 'enabled'
    name = '1'
#     data.run(testcases, state, name)
    data.check(state = None, device = 'hub')
    pass
    

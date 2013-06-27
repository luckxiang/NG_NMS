'''
Created on Mar 6, 2013

@author: me
'''

import time
from vsat import console
from string import upper
from ngnms import biaspoint
from threading import Thread
import os.path
from dlf import vsatdlf
from itertools import izip, count
import sys
import logging
from copy import deepcopy

FORMAT = '%(asctime)s (%(threadName)-8s) %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT,)


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

    def check(self, state = None, device = None, vsat_port = None):
        '''
        Check device availability.
        '''
        if device == 'vsat': self.vsat_status(state, vsat_port)
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

    def vsat_status(self, state = None, vsat_port = None):
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
            if vsat_port != None and str(vsat_port) != vsat[1]:
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

    def run(self, testcases, state = None, testname = None):
        '''
        Running test.
        '''
        header, states, cases = testcases
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

        # getting testcase0, initial working point.
        testcase0 = {}
        for state in states.keys():
            for row in states[state][sheet]:
                if int(states[state][sheet][row][1]) == 1:
                    testcase0 = cases[state][sheet][row]
                    break

        # show ngnms network tree.
        #self.check(state = None, device = 'hub')

        # getting active VSAT.
        vsats = {}
        for vsat in cases['enabled']['VSAT'].keys():
            vsat_data = cases['enabled']['VSAT'][vsat]
            vsat_ip = vsat_data.get('Console IP')
            vsat_port = int(vsat_data.get('Console PORT'))
            vsat_timeout = int(vsat_data.get('Connection timeout'))
            tries_timeout = int(vsat_data.get('Tries timeout'))
            number_of_tries = int(vsat_data.get('Number of tries'))
            vsat_channel = vsat_data.get('Channel Name')
            channel_number = vsat_data.get('Channel Number')
            vsats[vsat_port] = (vsat_ip, vsat_port, vsat_timeout, tries_timeout, 
                                            number_of_tries, vsat_channel, channel_number) 

        # Checking VSAT
        for vsat_port in vsats.keys():
            self.vsat_status(None, vsat_port)

        # all channels list:
        channels_list = []
        for vsat_port in vsats.keys():
            vsat = vsats[vsat_port]
            channels_list.append((vsat[-1], vsat_port))

        # creating result_data for each vsat.
        result_data = {}
        for vsat_port in vsats.keys():
            result_data[vsat_port] = {}

        for state in states_keys:
            print 'H'*60
            print upper(state).rjust(30)
            print 'H'*60
            print

            # creating resutl_data for states per vsat.
            for vsat_port in vsats.keys():
                result_data[vsat_port][state] = {}

            for row in sorted(states[state][sheet]):
                # storing just current row.
                current_case = states[state][sheet][row][1]
                # adjusting selecting test case.
                if sheet == 'TESTCASES': 
                    current_case = int(current_case)
                if testname != None and '%s' % testname != '%s' % current_case:
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
                #changed, url, ngnms_data = ngnms.set_ngnms_working_point(testcase)
                changed = False
                
                # checking vsat's bb up.
                def check_vsat_bb(*vsat_info):
                    '''
                    Setting vsat bb, and SR, reset board if needed.
                    '''
                    # getting vsat info.
                    vsat_ip, vsat_port, vsat_timeout, tries_timeout, number_of_tries = vsat_info
                    logging.debug('info:\> connecting: -> ip:{0} port:{1} timeout:{2}'.format(vsat_ip, vsat_port, vsat_timeout))
                    vsat = console.Grab(vsat_ip, vsat_port, vsat_timeout)
                    # waiting
                    logging.debug('info:\> waiting vsat up ...')
                    self.show_time_counter(20)
    
                    # setting param 34 and restarting board.
                    if changed:
                        logging.debug('status: OB symbol rate changed, waiting vsat up ...')
    
                        # changing 'rsp param set param 34' <ob_symbol_rate>
                        command = 'rsp param set param 34 %s' % testcase.get('OB symbol rate')
                        stop_pattern = '>'
                        logging.debug('info:\> %s' % command)
                        vsat.grab(command, stop_pattern)
                        # wait ...
                        self.show_time_counter(10)
                        # rebooting vsat..
                        command = 'rsp board reset board'
                        logging.debug('info:\> %s' % command)
                        stop_pattern = '>'
                        vsat.grab(command, stop_pattern)
                        wait_time = 60
                        self.show_time_counter(wait_time)
                    
                    # checking vsat_bb.
                    for nextstep in xrange(1, number_of_tries + 1):
                        logging.debug('step:\> nextstep -> %d' % nextstep)
                        # connect to vsat.
                        connected = vsat.connect()
                        link_status, message = vsat.check_bb()
                        logging.debug('status: %s' % message)
                        
                        # rebooting vsat if tried half number of tries.
                        if nextstep == (number_of_tries + 1)/2:
                            # rebooting vsat..
                            command = 'rsp board reset board'
                            logging.debug('info:\> %s' % command)
                            stop_pattern = '>'
                            vsat.grab(command, stop_pattern)
                            wait_time = 60
                            self.show_time_counter(wait_time)
                            
                        # checking if VSAT is ready: bb link up.
                        if connected and link_status:
                            logging.debug('status:\> VSAT Ready!')
                            break
                        else:
                            logging.debug('info:\> VSAT not READY!')
                            self.show_time_counter(tries_timeout)
                    else:
                        logging.debug('info:\> Exceeded [%s] number of tries per test case!' % number_of_tries)
                        # removing not activated vsat.
                        del vsats[vsat_port]

                # create threads for check_vsat_bb.
                th_vsat = {}
                for vsat_port in vsats.keys():
                    print "start:\> thread for vsat: %s" % vsat_port
                    th_vsat[vsat_port] = Thread(name = vsat_port, target = check_vsat_bb, args = vsats.get(vsat_port)[:-2])
                # start threads.
                for vsat_port in vsats.keys():
                    th_vsat[vsat_port].start()
                    time.sleep(0.3)
                # join threads with main program.
                for vsat_port in vsats.keys():
                    th_vsat[vsat_port].join()
                                              
                # checking vsats state.
                if not vsats:
                    # continue to next testcase if vsats has no vsat.
                    continue

                # setting DLF device for each VSAT.
                vsat_channels = {}
                for vsat_port in vsats.keys():
                    vsat = vsats[vsat_port]
                    channel_name = vsat[-2]
                    channel_number = vsat[-1]
                    vsat_ip, vsat_port, vsat_timeout = vsat[0:3]
                    vsat_param = dict(vsat_ip=vsat_ip, vsat_port=vsat_port, timeout=vsat_timeout) 
                    print '-'*60
                    print str(vsat_port).rjust(15), ':', vsat_ip, ':', vsat_port
                    print '-'*60
                    vsat_channels[vsat_port]=vsatdlf.dlf_controller(channel_number, channel_name, *channels_list, **vsat_param)

                """ == START: Thread function definition=== """
                def run_thread(*vsat_info):
                    '''
                    Run vsat thread
                    '''
                    # getting vsat info.
                    vsat_ip, vsat_port, vsat_timeout, tries_timeout, number_of_tries = vsat_info
                    logging.debug('info:\> connecting: -> ip:{0} port:{1} timeout:{2}'.format(vsat_ip, vsat_port, vsat_timeout))
                    vsat = console.Grab(vsat_ip, vsat_port, vsat_timeout)
                    
                    for nextstep in xrange(1, number_of_tries + 1):
                        logging.debug('step:\> nextstep -> %d' % nextstep)
                        # connect to vsat.
                        connected = vsat.connect()
                        link_status, message = vsat.check_bb()
                        logging.debug('status: %s' % message)
                        if connected and link_status:
                            duration = int(cases[state][sheet][row].get('Test duration'))
                            for ftptype in ['inbound', 'outbound']:
                                vsat.ftp_selftest(ftptype, duration)
                                logging.debug('step:\> %s -> start!' % ftptype)
                                self.show_time_counter(duration/2)
                                output = vsat.get_stats()
                                output['Channel'] = vsat_channels.get(vsat_port)
                                self.show_time_counter((duration/2) + 5)
                                # insert returned pkts stats to output.
                                output.update(vsat.get_pkts_stats())
                                if ftptype == 'inbound':
                                    nr_of_retransmited_ob_pckts = output['Number of OB retransmit packets']
                                    nr_of_transmited_ob_pckts = output['Number of transmitted OB packets']
                                    max_ob_bit_rate = output['Max IB bit rate [kbps]']
                                    cpu_ib = output.get('VSAT CPU [IB] [OB]')
                                else:
                                    output['Number of OB retransmit packets'] = nr_of_retransmited_ob_pckts
                                    output['Number of transmitted OB packets'] = nr_of_transmited_ob_pckts
                                    output['Max IB bit rate [kbps]'] = max_ob_bit_rate
                                    output['VSAT CPU [IB] [OB]'] = '[%s]/[%s]' % (cpu_ib.strip('$'), output.get('VSAT CPU [IB] [OB]').strip('$'))
                                logging.debug('status: %s -> done!' % ftptype)
                            break
                        else:
                            logging.debug('info:\> VSAT not READY!')
                            self.show_time_counter(tries_timeout)
                    else:
                        logging.debug('info:\> Exceeded [%s] number of tries per test case!' % number_of_tries)
                        return
                    # printing ready data to output
                    logging.debug('%s TEST: %s %s' % ('-'*24, current_case, '-'*24))
                    result_data[vsat_port][state][row] = deepcopy(cases[state][sheet][row])
                    #logging.debug('%s %s', id(cases[state][sheet][row]), id(result_data[vsat_port][state][row]))
                    for key in header[sheet][0]:
                        # print step to screen.
                        time.sleep(0.1)
                        if key in output.keys():
                            result_data[vsat_port][state][row][key] = output[key]
                        if key == 'Max IB bit rate [kbps]':
                            logging.debug('%s OUTPUT: %s %s' % ('-'*24, current_case, '-'*24))
                        logging.debug('{0:38} = {1:30}'.format(key, str(result_data[vsat_port][state][row][key])))
                    logging.debug('')
                    logging.debug('-'*60)
                    logging.debug('')
                    # saving data to excel file.
                    output_xlfile = '%s_output.xls' % vsat_port
                    output_dir = 'data/output'
                    output_file = os.path.join(output_dir, output_xlfile)
                    
                    # Check if file is closed.
                    while True:
                        try:
                            if os.path.isfile(output_file):
                                os.remove(output_file)
                        except Exception as e:
                            print e
                            # file already exists, try again
                            print
                            print 'Please close file first [%s], then continue: ' % output_file,
                            raw_input('-> [ENTER]')
                            continue
                        break

                    logging.debug('info:\> Saving result to [%s] excel file!' % output_file)
                    self.save_row_to_excel(header[sheet][0], result_data[vsat_port], output_file)
                """ === END: Thread function ==="""

                # create threads for run_thread.
                tvsat = {}
                for vsat_port in vsats.keys():
                    print "start:\> thread for vsat: %s" % vsat_port
                    tvsat[vsat_port] = Thread(name = vsat_port, target = run_thread, args = vsats.get(vsat_port)[:-2])
                # start threads.
                for vsat_port in vsats.keys():
                    tvsat[vsat_port].start()
                    time.sleep(0.3)
                # join threads with main program.
                for vsat_port in vsats.keys():
                    tvsat[vsat_port].join()

        # changing to initial working point.
        print 'step:\> changing to initial working point' 
        changed, url, ngnms_data = ngnms.set_ngnms_working_point(testcase0)

        # restoring vsats SR from testcase0 (default).
        def init_vsat(*vsat_info):
            '''
            Set vsat SR to default, testcase0
            '''
            vsat_ip, vsat_port, vsat_timeout, tries_timeout, number_of_tries = vsat_info
            vsat = console.Grab(vsat_ip, vsat_port, vsat_timeout)
            logging.debug('status:\> default vsat symbol rate')
            # changing 'rsp param set param 34' <ob_symbol_rate>
            command = 'rsp param set param 34 %s' % testcase0.get('OB symbol rate')
            stop_pattern = '>'
            logging.debug('info:\> %s' % command)
            vsat.grab(command, stop_pattern)
            # wait ...
            self.show_time_counter(5)
            # rebooting vsat..
            command = 'rsp board reset board'
            logging.debug('info:\> %s' % command)
            stop_pattern = '>'
            vsat.grab(command, stop_pattern)

        # setting param 34 and restarting board
        # using function: init_vsat from above.
        if changed:
            for vsat_port in vsats.keys():
                tvsat[vsat_port] = Thread(name = vsat_port, target = init_vsat, args = vsats.get(vsat_port)[:-2])
            for vsat_port in vsats.keys():
                tvsat[vsat_port].start()
                time.sleep(0.3)
            for vsat_port in vsats.keys():
                tvsat[vsat_port].join()
                

        # greetings 
        print
        print '-'*60
        print "\n\t\tGood job!\n\t\tCongratulations! @};-\n\t\tWell done!\n"
        print '-'*60

    def save_row_to_excel(self, header, result_data, output_xlfile):
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
        for state in result_data.keys():
            # Set row style.
            if state == 'enabled':
                style = styleEnabled
            elif state == 'disabled':
                style = styleDisabled
            for row in result_data[state].keys():
                for cell in header[32:]:
                    wb.get_sheet(1).write(row, header.index(cell), result_data[state][row].get(cell), style)

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
                logging.debug('H'*60)
                logging.debug('SUCCESS!: Successfully saved data to file: [%s]!' % output_xlfile)
                logging.debug('H'*60)
                break

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
    
def run(xlfile, state = None, testname = None):
    '''
    Run testcase(s}.
    '''
    ngnms = Selftest(xlfile)
    testcases = ngnms.get_testcases()
    ngnms.run(testcases, state, testname)

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
    

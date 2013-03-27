'''
Created on Mar 9, 2013

@author: me
'''
import xlrd
import sys
from string import upper
from time import sleep

row_print_speed = 0.35

class Xls:
    '''
    Excel XLS file reader.
    '''
    logger = False

    def __init__(self, xlsfile):
        '''
        Get excel XLS file.
        '''
        self.xlsfile = xlsfile
        
    def get_testcases(self):
        '''
        Open Test Cases file
        '''
        # check if file exist.
        try:
            with open(self.xlsfile): pass
        except Exception as e:
            print
            print '*'*60
            print e
            print '*'*60
            sys.exit()

        # read all data from excel file.
        workbook = xlrd.open_workbook(self.xlsfile)
        worksheets = workbook.sheet_names()
        header = {}
        testcases = {}
        for sheet in worksheets:
            # skipping INFO sheet.
            if sheet == 'INFO': continue
            worksheet = workbook.sheet_by_name(sheet)
            header[sheet] = {}
            testcases[sheet] = {}
            for current_row in xrange(worksheet.nrows):
                if current_row == 0:
                    header[sheet][current_row] = []
                # excluding row 1,2 if sheet is TESTCASES.
                elif sheet == 'TESTCASES' and current_row in [1, 2]:
                    continue
                else:
                    testcases[sheet][current_row] = []
                for current_cell in xrange(worksheet.ncols):
                    cell_value = worksheet.cell_value(current_row, current_cell)
                    if current_row == 0:
                        header[sheet][current_row].append(cell_value)
                        continue
                    else:
                        testcases[sheet][current_row].append(cell_value)

        # adjusting header
        temp = header['TESTCASES'][0]
        for name in ['IB symbol rate', 'IB mode code', 'Number of Channels', 'Dynamic/Static', 'Symbol Rate']:
            index = temp.index(name)
            if name == 'Symbol Rate':
                counter = 0
                for line in xrange(1,5):
                    for col in xrange(1,3):
                        temp[index + counter] = '%s %s%s' % (name, line, col)
                        counter += 1
            else:
                for counter in xrange(4):
                    temp[index + counter] = '%s %s' % (name, counter + 1)

        # sort active and inactive test cases.
        active = {}
        inactive = {}
        for sheet in testcases.keys():
            active[sheet] = {}
            inactive[sheet] = {}
            for row in testcases[sheet]:
                if testcases[sheet][row][0] is not '':
                    active[sheet][row] = []
                else:
                    inactive[sheet][row] = []
                for cell in testcases[sheet][row]:
                    if testcases[sheet][row][0] is not '':
                        active[sheet][row].append(cell)
                    else:
                        inactive[sheet][row].append(cell)
        
        # combine into states of active and inactive test cases.
        states = {'active':active, 'inactive':inactive}
        testcases = (header, states)

        # display output
        if self.logger:
            self.display(testcases)
        
        # return headers, active and inactive test cases.
        return testcases

    def display(self, testcases, statename = None, sheetname = None):
        '''
        Display testcases.
        '''

        header, states = testcases

        if statename == None:
            states_keys = states.keys()
        else:
            states_keys = [statename]

        for state in states_keys:
            print 'H'*60
            print upper(state).rjust(30)
            print 'H'*60
            if sheetname == None:
                sheets_keys = states[state].keys()
            else:
                sheets_keys = [sheetname]
                
            for sheet in sheets_keys:
                print 'x'*60
                print upper('%s : %s' % (sheet, state)).rjust(35)
                print 'x'*60
                for row in sorted(states[state][sheet]):
                    current_case = states[state][sheet][row][1]
                    print '-'*60
                    print upper('%s : %s : %s' % (sheet, current_case, state)).rjust(38)
                    print '-'*60
                    sleep(row_print_speed)
                    for key, value in zip(header[sheet][0], states[state][sheet][row]):
                        print '{0:40} = {1:20}'.format(key, str(value))

if __name__ == "__main__":
    '''
    Main program.
    '''
    data = Xls('../data/demo.xls')
    #data.logger = True
    testcases = data.get_testcases()
    data.display(testcases)
#     header, states = testcases
#     for state in states.keys():
#         for sheet in states[state].keys():
#             for row in states[state][sheet].keys():
#                 # print row, state, sheet, states[state][sheet][row]
#                 print state,
#                 for cell in states[state][sheet][row]:
#                     print cell,
#                 print
    
    data = Xls('../data/test.xls')
    data.logger = True
    data.get_testcases()
    pass
        
'''
Created on Mar 9, 2013

@author: me
'''
import xlrd
import sys
from string import upper

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
                    if isinstance(cell_value, float): 
                        cell_value = str(int(cell_value))
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
                        temp[index + counter] = '%s_%s.%s' % (name, line, col)
                        counter += 1
            else:
                for counter in xrange(4):
                    temp[index + counter] = '%s_%s' % (name, counter + 1)

        # sort enabled and disabled test cases.
        enabled = {}
        disabled = {}
        for sheet in testcases.keys():
            enabled[sheet] = {}
            disabled[sheet] = {}
            for row in testcases[sheet]:
                if testcases[sheet][row][0] is not '':
                    enabled[sheet][row] = []
                else:
                    disabled[sheet][row] = []
                for cell in testcases[sheet][row]:
                    if testcases[sheet][row][0] is not '':
                        enabled[sheet][row].append(cell)
                    else:
                        disabled[sheet][row].append(cell)

        
        # combine into states of enabled and disabled test cases.
        states = {'enabled':enabled, 'disabled':disabled}

        # create test cases hash
        cases = {}
        for state in states.keys():
            cases[state] = {}
            for sheet in header.keys():
                cases[state][sheet] = {}
                for row in states[state][sheet]:
                    cases[state][sheet][row] = {}
                    for key, value in zip(header[sheet][0], states[state][sheet][row]):
                        if isinstance(value, float): 
                            value = str(int(value))
                        cases[state][sheet][row][key] = value
        
        testcases = (header, states, cases)
        # display output
        if self.logger:
            self.display(testcases)
        
        # return headers, enabled and disabled test cases.
        return testcases

    def display(self, testcases, sheetname = None, name = None, *statename):
        '''
        Display testcases.
        '''

        header, states, cases = testcases

        if len(statename) != 1:
            states_keys = reversed(states.keys())
        else:
            states_keys = statename

        for state in states_keys:
            print 'H'*60
            print upper(state).rjust(30)
            print 'H'*60
            if sheetname != None and sheetname in header.keys():
                sheets_keys = [sheetname]
            else:
                sheets_keys = states[state].keys()
                
            for sheet in sheets_keys:
                print 'x'*60
                print upper('%s : %s' % (sheet, state)).rjust(35)
                print 'x'*60
                for row in sorted(states[state][sheet]):
                    current_case = states[state][sheet][row][1]

                    # adjusting selecting test case.
                    if sheet == 'TESTCASES': current_case = int(current_case)
                    if name != None and '%s' % name != '%s' % current_case:
                        print '{0}: {1}'.format(sheet, current_case)
                        continue
                    print '-'*60
                    print upper('%s : %s : %s' % (sheet, current_case, state)).rjust(38)
                    print '-'*60
                    for key, value in zip(header[sheet][0], states[state][sheet][row]):
                        print '  {0:.<40} = {1:20}'.format(key, str(value))
                    print '-'*60

if __name__ == "__main__":
    '''
    Main program.
    '''
    data = Xls('../data/demo.xls')
    #data.logger = True
    testcases = data.get_testcases()
    data.display(testcases)

    data = Xls('../data/test.xls')
    data.logger = True
    data.get_testcases()
    pass
        
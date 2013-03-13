'''
Created on Mar 9, 2013

@author: me
'''
import openpyxl

class Xlsx:
    '''
    Excel XLSX file reader.
    '''
    logger = False

    def __init__(self, xlsxfile):
        '''
        Get excel XLSX file.
        '''
        self.xlsxfile = xlsxfile
        
    def get_testcases(self):
        '''
        Open Test Cases file
        '''
        workbook = openpyxl.load_workbook(filename = self.xlsxfile, use_iterators = True)
        worksheets = workbook.get_sheet_names()
        testcases = {}
        for sheet in worksheets:
            worksheet = workbook.get_sheet_by_name(sheet)
            # print "--"*10, 'SHEET:', sheet, "--"*10
            testcases[sheet] = {}
            header = []
            for row in worksheet.iter_rows():
                curr_row = row[0][0] - 1
                # print 'Row:', curr_row
                testcases[sheet][curr_row] = {}
                # getting sheet header.
                if curr_row == 0:
                    for cell in row:
                        header.append(cell.internal_value)
                title = 0
                for cell in row:
                    # print ' '*4, cell.data_type,':', cell.internal_value
                    testcases[sheet][curr_row][header[title]] = cell.internal_value
                    title = title + 1
            # print len(header), header
        # print testcases
        if self.logger:
            self.display(testcases)
              
        return testcases
        
    def display(self, testcases):
        '''
        Display testcases.
        '''
        for sheet in testcases.keys():
            print
            print "-"*20, 'SHEET:', sheet, "-"*20
            for row in testcases[sheet].keys():
                # print row, ' - ', testcases[sheet][row]
                print
                print 'Row:', row
                for cell in testcases[sheet][row].keys():
                    # print ' '*4, cell, '=', testcases[sheet][row][cell]
                    print ' '*5, '{0:35} = {1:40}'.format(str(cell), str(testcases[sheet][row][cell]))
                    

if __name__ == "__main__":
    
    data = Xlsx('../data/test.xlsx')
    data.logger = True
    data.get_testcases()

'''
Created on Mar 9, 2013

@author: me
'''
import xlrd

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
        workbook = xlrd.open_workbook(self.xlsfile)
        worksheets = workbook.sheet_names()
        testcases = {}
        for sheet_name in worksheets:
            header = []
            worksheet = workbook.sheet_by_name(sheet_name)
            # print "--"*10, 'SHEET:',sheet_name, "--"*10
            # print '# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank'
                        
            testcases[sheet_name] = {}
            num_rows = worksheet.nrows - 1
            num_cells = worksheet.ncols - 1
            curr_row = -1
            while curr_row < num_rows:
                curr_row += 1
                # row = worksheet.row(curr_row)
                # print row
                testcases[sheet_name][curr_row] = {}
                if curr_row == 0:
                    curr_cell = -1
                    while curr_cell < num_cells:
                        curr_cell += 1
                        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                        # cell_type = worksheet.cell_type(curr_row, curr_cell)
                        cell_value = worksheet.cell_value(curr_row, curr_cell)
                        header.append(cell_value)
                # print 'Row:', curr_row
                curr_cell = -1
                while curr_cell < num_cells:
                    curr_cell += 1
                    # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                    # cell_type = worksheet.cell_type(curr_row, curr_cell)
                    cell_value = worksheet.cell_value(curr_row, curr_cell)
                    # print '    ', cell_type, ':', cell_value
                    if cell_value == '':
                        cell_value = None
                    testcases[sheet_name][curr_row][header[curr_cell]] = cell_value

        # print testcases
        if self.logger:
            self.display(testcases)
        # return all data from excel file.
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
    
    data = Xls('../data/test.xls')
    data.logger = True
    data.get_testcases()
    pass
        
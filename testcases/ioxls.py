'''
Created on Mar 9, 2013

@author: me
'''

class Xls:
    '''
    classdocs
    '''


    def __init__(self, xlsfile, csvfile):
        '''
        Constructor
        '''
        self.xlsfile = xlsfile
        self.csvfile = csvfile
        
    def openTS(self):
        '''
        Open Test Cases file
        '''
        from xlrd import open_workbook
        
        import csv
        with open(self.csvfile, 'wb') as f:
            writer = csv.writer(f)

            workbook = open_workbook(self.xlsfile)
            worksheet = workbook.sheet_by_name('Matrix')
            num_rows = worksheet.nrows - 1
            num_cells = worksheet.ncols - 1
            curr_row = -1
            while curr_row < num_rows:
                curr_row += 1
                curr_cell = -1
                row_list = []
                while curr_cell < num_cells:
                    curr_cell += 1
                    # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                    cell_value = worksheet.cell_value(curr_row, curr_cell)
                    try:
                        cell_value = int(cell_value)
                    except:
                        pass
                    row_list.append(cell_value)
                print 'Row: %d %s' % (curr_row, row_list)
                writer.writerow(row_list)
        
if __name__ == "__main__":
    
    test = Xls("../data/TestMatrix.xls", "../data/some.csv")
    test.openTS()
        
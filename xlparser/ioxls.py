'''
Created on Mar 9, 2013

@author: me
'''
import csv
from xlrd import open_workbook

class Xls:
    '''
    classdocs
    '''


    def __init__(self, xlsfile):
        '''
        Constructor
        '''
        self.xlsfile = xlsfile
        
    def export_sheet_to_csv(self, sheetname, csvfile):
        '''
        Open Test Cases file
        '''

        with open(csvfile, 'wb') as f:
            writer = csv.writer(f)

            workbook = open_workbook(self.xlsfile)
            worksheet = workbook.sheet_by_name(sheetname)
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
                writer.writerow(row_list)
                
if __name__ == "__main__":
    
    pass
        
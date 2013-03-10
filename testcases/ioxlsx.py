'''
Created on Mar 9, 2013

@author: me
'''

class Xlsx:
    '''
    classdocs
    '''


    def __init__(self, xlsxfile, csvfile):
        '''
        Constructor
        '''
        self.xlsxfile = xlsxfile
        self.csvfile = csvfile
        
    def openTS(self):
        '''
        Open Test Cases file
        '''
        
        import csv
        with open(self.csvfile, 'wb') as f:
            writer = csv.writer(f)

            from openpyxl import load_workbook
            workbook = load_workbook(filename = self.xlsxfile, use_iterators = True)
            print workbook.get_sheet_names()
            worksheet = workbook.get_sheet_by_name(name = 'Matrix')
            
            
            for row in worksheet.iter_rows():
                row_list = []
                for cell in row:
                    try:
                        cell_value = cell.internal_value
                        cell_value = int(cell_value)
                    except:
                        pass
                    print cell_value,
                    row_list.append(cell_value)
                print
                writer.writerow(row_list)

if __name__ == "__main__":
    
    test = Xlsx("../data/TestMatrix.xlsx", "../data/some.csv")
    test.openTS()
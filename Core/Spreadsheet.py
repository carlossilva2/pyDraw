from os import listdir, mkdir
from xlsxwriter import Workbook

class Spreadsheet:
    def __init__(self, name):
        if "Spreadsheets" not in listdir("."):
            mkdir("Spreadsheets")
        self.book = Workbook("Spreadsheets/{0}.xlsx".format(name))
        self.worksheet = self.book.add_worksheet()
        self.BOLD = self.book.add_format({"bold": True})
        self.ITALIC = self.book.add_format({"italic": True})

    def write(self, cell, data, format=None):
        if format is None:
            self.worksheet.write(str(cell), data)
        else:
            self.worksheet.write(str(cell), data, format)

    def write_num_notation(self, row, column, data, format):
        if type(row) is not int or type(column) is not int:
            raise TypeError("Row and Column must be integers")
            exit(1)

        if format is None:
            self.worksheet.write(row, column, data)
        else:
            self.worksheet.write(row, column, data, format)

    def add_image(self, row, column, path):
        if type(row) is not int or type(column) is not int:
            raise TypeError("Row and Column must be integers")
            exit(1)
        self.worksheet.insert_image(row, column, str(path))

    def format_column(self, column, spacing):
        if len(column) > 1:
            print("Column must be a single character")
        else:
            self.worksheet.set_column(
                "{0}:{0}".format(column.upper()), spacing)

    def finish(self):
        self.book.close()

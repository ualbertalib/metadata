import openpyxl
from openpyxl import Workbook

wb = Workbook()
wb = openpyxl.load_workbook('Untitled 1.xlsx')
names = wb.get_sheet_names()
li = {}
ws = wb['Sheet1']
for i in range(1, ws.max_row+1):
	key = str(ws.cell(row=i, column=1).value.replace('http://example.org/', '').split('#')[0])
	vf = str(ws.cell(row=i, column=2).value)
	lc = str(ws.cell(row=i, column=3).value)
	li[key] = {'vf' : vf, 'lc' : lc}
print (li)


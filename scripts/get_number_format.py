from openpyxl import load_workbook
wb=load_workbook("/Users/wwukong/Downloads/ans/部门成绩/考核组评委.xlsx")
ac=wb.active
print(ac["B2"].number_format)
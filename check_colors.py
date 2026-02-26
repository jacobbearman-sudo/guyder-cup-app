import openpyxl
wb = openpyxl.load_workbook('/Users/jb/Desktop/The Guyder Cup.xlsx', data_only=True)
ws = wb['2022 Wheels Up']
for row in ws.iter_rows(min_row=24, max_row=41):
    row_num = row[0].row
    d_val = str(row[3].value) if row[3].value else ''
    e_val = str(row[4].value) if row[4].value else ''
    f_val = str(row[5].value) if row[5].value else ''
    d_fill = row[3].fill
    e_fill = row[4].fill
    d_color = d_fill.fgColor.rgb if d_fill and d_fill.fgColor else 'none'
    e_color = e_fill.fgColor.rgb if e_fill and e_fill.fgColor else 'none'
    d_font = row[3].font
    e_font = row[4].font
    d_bold = d_font.bold if d_font else False
    e_bold = e_font.bold if e_font else False
    if d_val or e_val or f_val:
        print(f'Row {row_num}: D={d_val} (bold={d_bold}, color={d_color}), E={e_val} (bold={e_bold}, color={e_color}), F={f_val}')

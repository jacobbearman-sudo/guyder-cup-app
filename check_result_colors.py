import openpyxl
wb = openpyxl.load_workbook('/Users/jb/Desktop/The Guyder Cup.xlsx', data_only=True)
ws = wb['2022 Wheels Up']
for row in ws.iter_rows(min_row=24, max_row=41):
    row_num = row[0].row
    d_val = str(row[3].value) if row[3].value else ''
    e_val = str(row[4].value) if row[4].value else ''
    f_val = str(row[5].value) if row[5].value else ''
    f_fill = row[5].fill
    f_fg = f_fill.fgColor.rgb if f_fill and f_fill.fgColor else 'none'
    f_bg = f_fill.bgColor.rgb if f_fill and f_fill.bgColor else 'none'
    f_font_color = row[5].font.color.rgb if row[5].font.color and row[5].font.color.rgb else 'none'
    if d_val or e_val or f_val:
        print(f'Row {row_num}: result={f_val}, fill_fg={f_fg}, fill_bg={f_bg}, font_color={f_font_color}')

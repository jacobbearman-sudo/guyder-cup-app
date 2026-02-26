import openpyxl

wb = openpyxl.load_workbook('/Users/jb/Desktop/The Guyder Cup.xlsx', data_only=True)
ws = wb['2025 Battle for Sarah']

print('=== 2025 Battle for Sarah - Raw data with all columns ===')
for row in ws.iter_rows(min_row=20, max_row=45):
    row_num = row[0].row
    vals = []
    for i, c in enumerate(row[:12]):
        v = str(c.value).strip() if c.value else ''
        fill = c.fill
        fg = fill.fgColor.rgb if fill and fill.fgColor else '00'
        vals.append(f'{v}[{fg}]')
    print(f'Row {row_num}: {" | ".join(vals)}')

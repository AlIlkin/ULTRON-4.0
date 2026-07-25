import win32com.client

def create_table(rows, cols):
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True

    wb = excel.Workbooks.Add()
    sheet = wb.ActiveSheet

    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            sheet.Cells(r, c).Value = f"R{r}C{c}"
    return "Table created in Excel."
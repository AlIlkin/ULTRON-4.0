import win32com.client

def write_essay(text, font="Calibri", size=11):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = True

    doc = word.Documents.Add()
    selection = word.Selection

    selection.Font.Name = font
    selection.Font.Size = size
    selection.TypeText(text)

from action_engine import platform

def write_essay(text, font="Calibri", size=11):
    word = platform.system().client.Dispatch("Word.Application")
    word.Visible = True

    doc = word.Documents.Add()
    selection = word.Selection

    selection.Font.Name = font
    selection.Font.Size = size
    selection.TypeText(text)

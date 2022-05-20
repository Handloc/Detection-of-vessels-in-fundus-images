from gui import GUI
import wx

app = wx.App()
frame = GUI(None, title='Wykrywanie naczyń dna siatkówki oka', size=(1200, 650))
frame.Show()
app.MainLoop()

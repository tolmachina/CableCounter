from tkinter import *
from main import *
from tkinter import ttk

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

def myClick():
    get_data_pdf(myInputField.get())

myInputField = Entry(root)
myLabel = Label(root, text = "Calculating cables for d&b system")
myButton = Button(root, text = "Load Array PDF File with setup data", command = myClick, bg = 'grey')

myLabel.grid()
myButton.pack()
myInputField.pack()

root.mainloop()

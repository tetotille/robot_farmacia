from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk


root = Tk()

root.title("Mecabot")

#icon
p1 = PhotoImage(file = 'img/images.png')
root.iconphoto(False, p1)

canvas = Canvas(root, width=600, height=300)
canvas.grid(columnspan=3)

#logo
logo = Image.open("img/logo.png")
logo = ImageTk.PhotoImage(logo)
logo_label = Label(image=logo)
logo_label.grid(column=1, row=0)

#instructions
instructions = Label(root, text='Bienvenido al robot farmacéutico Mecabot, si desea algún medicamento, presione \nel botón "Escanear Código QR" y proceda a escanear el código del medicamento.\n\n También puede listar los medicamentos disponibles presionando el botón de \n"Listar medicamentos".',font=("Ubuntu", 12))
instructions.grid(columnspan=3, column=0, row=1)

#Scanner Button
scanner_text = StringVar()
scanner_button = Button(root, textvariable=scanner_text)
scanner_text.set("Escanear Código QR")
scanner_button.grid(column=1, row=2)

root.mainloop()

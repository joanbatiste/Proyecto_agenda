from tkinter import *
from tkinter import ttk

import contenido.login

class Aplicacion:
    def __init__(self):
        self.ventana1 = Tk()
        self.ventana1.geometry("350x350")
        self.ventana1.title("Bienvenido")
        Label(self.ventana1, text = "Para acceder a la agenda debes ser usuario registrado", fg = "blue").pack()
        

        self.botonInicio = Button(self.ventana1, text = "Inicio", command = self.Empezar)
        self.botonInicio.pack()
        self.botonInicio.place(relx = 0.25, rely = 0.25, relwidth = 0.50, relheight = 0.15)

        self.botonSalir = Button( self.ventana1, text = "Salir", command = lambda:self.ventana1.quit())
        self.botonSalir.pack()
        self.botonSalir.place(relx = 0.25, rely = 0.55, relwidth = 0.50, relheight = 0.15)

        self.ventana1.mainloop()


    def Empezar(self):
        contenido.login.Mostrar()



aplicacion1 = Aplicacion()
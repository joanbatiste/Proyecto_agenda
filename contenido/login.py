from tkinter import *
from contenido.DataBase import CrearConexion, CrearCursor, CrearTablaContactos, CrearTablaUsuarios
from tkinter import ttk
import pymysql
from tkinter import messagebox
import contenido.contactos
import datetime
import hashlib
conexion = CrearConexion("b6bauoez7gkwtblar05j")
cursor = CrearCursor(conexion)

class Ventana_login():

    def __init__(self):
        self.menu_inicio = Tk()
        self.menu_inicio.geometry("320x320")
        self.menu_inicio.title("Acceso Usuarios")

        # Botones de acceso y de registro para usuarios
        self.message = Label(self.menu_inicio, text = "Seleccione opción")
        self.message.place(relx = 0.15 , rely = 0.10, relwidth = 0.7, relheight = 0.10)
        self.botonAcceso = Button(self.menu_inicio, text = "Acceso", command = self.AccesoUsuario)
        self.botonAcceso.pack()
        self.botonAcceso.place(relx = 0.25, rely = 0.25, relwidth = 0.50, relheight = 0.15)

        self.botonRegistro = Button(self.menu_inicio, text = "Registro", command = self.RegistroUsuario)
        self.botonRegistro.pack()
        self.botonRegistro.place(relx = 0.25, rely = 0.55, relwidth = 0.50, relheight = 0.15)

        self.message1 = Label(self.menu_inicio, text = "", fg = "green")
        self.message1.place(relx = 0.10, rely = 0.90, relwidth = 0.8, relheight = 0.10)

    # Función para acceso de usuarios registrados
    def AccesoUsuario(self):
        self.ventana_acceso = Toplevel()
        self.ventana_acceso.title("Usuario registrado")
        self.ventana_acceso.geometry("300x300")

        Label(self.ventana_acceso, text = "Introduce tu usuario y contraseña").place(relx = 0.13, rely =0.02, relwidth = 0.7, relheight = 0.10)
        Label(self.ventana_acceso, text = "Nombre de usuario: ").place(relx = 0.15 , rely = 0.12, relwidth = 0.7, relheight = 0.10)
        usuario = Entry(self.ventana_acceso)
        usuario.place(relx = 0.25, rely = 0.22, relwidth = 0.50, relheight = 0.15)

        Label(self.ventana_acceso, text = "Contraseña: ").place(relx = 0.15 , rely = 0.40, relwidth = 0.7, relheight = 0.10)
        contraseña = Entry(self.ventana_acceso,show = "*")
        contraseña.place(relx = 0.25, rely = 0.50, relwidth = 0.50, relheight = 0.15)

        Button(self.ventana_acceso, text = "Acceder", command = lambda:self.Acceder(usuario.get(), contraseña.get())).place(relx = 0.25, rely = 0.75, relwidth = 0.50, relheight = 0.15)

    # Ventana para registro de nuevos usuarios
    def RegistroUsuario(self):
        self.ventana_registro = Toplevel()
        self.ventana_registro.title("Nuevos usuarios")
        self.ventana_registro.geometry("300x300")

        Label(self.ventana_registro, text = "Escoge tu usuario y contraseña").place(relx = 0.13, rely =0.02, relwidth = 0.7, relheight = 0.10)
        Label(self.ventana_registro, text = "Nombre de usuario").place(relx = 0.12 , rely = 0.12, relwidth = 0.7, relheight = 0.10)
        usuario = Entry(self.ventana_registro)
        usuario.place(relx = 0.25, rely = 0.22, relwidth = 0.40, relheight = 0.10)

        self.boton_comprobar = Button(self.ventana_registro, text = "Comprobar", command = lambda:self.Usuario_Registrado( usuario.get()))
        self.boton_comprobar.place(relx = 0.67, rely = 0.22, relwidth = 0.30, relheight = 0.10)        
        
        Label(self.ventana_registro, text = "Contraseña: ").place(relx = 0.12 , rely = 0.43, relwidth = 0.7, relheight = 0.10)
        contraseña = Entry(self.ventana_registro, show = "*")
        contraseña.place(relx = 0.25, rely = 0.53, relwidth = 0.40, relheight = 0.10)

        self.boton_registro = Button(self.ventana_registro, text = "Registrarse", command=lambda:self.Registrarse(usuario.get(), contraseña.get()))
        
        self.boton_registro.place_forget()

    # Comprobar si el usuario esta registrado:
    def Usuario_Registrado(self, usuario):
        query = "SELECT * FROM Usuarios WHERE usuario = %s "
        parameters = (usuario,)
        cursor.execute(query, parameters)
        datos_registro = cursor.fetchall()
        if datos_registro:
            self.message = Label(self.ventana_registro, text = "", fg = "red")
            self.message.place(relx = 0.20, rely = 0.33, relwidth = 0.8, relheight = 0.10)
            self.message['text'] = "El usuario ya existe"
        else:
            self.message = Label(self.ventana_registro, text = "", fg = "green")
            self.message.place(relx = 0.20, rely = 0.33, relwidth = 0.8, relheight = 0.10)
            self.message['text'] = "Usuario disponible"
            self.boton_registro.place(relx = 0.25, rely = 0.73, relwidth = 0.40, relheight = 0.10)

    # Función para guardar los datos de registro del usuario en la BD
    def Registrarse(self, usuario,contraseña):
        query = 'INSERT INTO Usuarios(usuario, contraseña) VALUES (%s,SHA2(%s, 256))'
        encriptada = contraseña
        encriptada = encriptada.encode()
        h = hashlib.sha256(encriptada)
        pass_encript = h.digest()
        print(h.digest())
        parameters = (usuario, pass_encript)
        cursor.execute(query, parameters)
        conexion.commit()
        self.ventana_registro.destroy()
        self.message1['text'] = "Usuario creado satisfactoriamente"

    # Función para dar acceso a la agenda al usuario registrado
    def Acceder(self, usuario, contraseña):
        query = "SELECT * FROM Usuarios WHERE usuario = %s AND contraseña = SHA2(%s,256)"
        encriptada = contraseña
        encriptada = encriptada.encode()
        h = hashlib.sha256(encriptada)
        pass_encript = h.digest()
        parameters = (usuario, pass_encript)
        cursor.execute(query, parameters)
        datos_usuario = cursor.fetchall() 
        
        if datos_usuario: #Si esta registrado, abre la agenda e inserta el usuario en la tabla Logueado
            messagebox.showinfo(message = "Usuario y contraseña correctos", title = "Login Correcto")
            usuario_logueado = (datos_usuario[0][1])
            currenttime = str(datetime.datetime.now())
            cursor.execute("INSERT INTO Logueado (Nombre, Fecha) VALUES ('"+usuario_logueado+"', '"+currenttime+"') ")
            conexion.commit()
            self.ventana_acceso.destroy()
            self.menu_inicio.destroy()
            contenido.contactos.Mostrar_Menu()                                   
        else :
            messagebox.showinfo(message = "Usuario o contraseña incorrectos", title = "Login Incorrecto")
    

def Mostrar():
    aplicacion1 = Ventana_login()




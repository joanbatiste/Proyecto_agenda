from tkinter import *
from tkinter import ttk
from contenido.DataBase import CrearConexion, CrearCursor, CrearTablaContactos, CrearTablaUsuarios
import pymysql

conexion = CrearConexion("b6bauoez7gkwtblar05j")
cursor = CrearCursor(conexion)

# Funcion para mostrar en pantalla el usuario que esta trabajando con la agenda
def UsuarioLogueado():
        query = "SELECT Nombre FROM Logueado ORDER BY ID DESC LIMIT 1"
        cursor.execute(query)
        logueado = cursor.fetchone()
        return logueado[0]

class Ventana():
    def __init__(self):
        # Defino la ventana principal y su título

        self.master = Tk()
        self.master.title("Bienvenido a tu Agenda de Contactos")
        self.master.geometry("420x420")

        # Identificación de usuario logueado
        
        Label(self.master , text = "usuario: "+ UsuarioLogueado() , fg = "blue").place(relx = 0.02, rely = 0.005 )
                        
        # Creamos los botones de la ventana principal

        self.botonCrearContacto = Button(self.master, text="Nuevo", command=self.CrearContacto)
        self.botonCrearContacto.pack()
        self.botonCrearContacto.place(relx = 0.42, rely = 0.12, relwidth = 0.20, relheight = 0.10)

        self.botonActualizarContacto = Button(self.master, text="Editar", command=self.EditarContacto)
        self.botonActualizarContacto.pack()
        self.botonActualizarContacto.place(relx = 0.42, rely = 0.28, relwidth = 0.20, relheight = 0.10)

        self.botonEliminarContacto = Button(self.master, text="Elilminar", command=self.EliminarContacto)
        self.botonEliminarContacto.pack()
        self.botonEliminarContacto.place(relx = 0.42, rely = 0.45, relwidth = 0.20, relheight = 0.10)

        self.botonBuscarContacto = Button(self.master, text="Buscar", command=self.BuscarContacto)
        self.botonBuscarContacto.pack()
        self.botonBuscarContacto.place(relx = 0.42, rely = 0.62, relwidth = 0.20, relheight = 0.10)

        self.botonSalir = Button(self.master, text="Salir", command=self.SalirAgenda)
        self.botonSalir.pack()
        self.botonSalir.place(relx = 0.42, rely = 0.78, relwidth = 0.20, relheight = 0.10)
    
        self.message = Label(self.master, text = "", fg = "red")
        self.message.place(relx = 0.15, rely = 0.88, relwidth = 0.8, relheight = 0.10)
    
    
    
    # Creamos un nuevo contacto en la agenda

    def CrearContacto(self):
        self.ventana_crear = Toplevel() 
        self.ventana_crear.title = "Crear Contacto"

        Label(self.ventana_crear, text = 'Nombre: ').grid(row = 0, column = 1)
        nombre = Entry(self.ventana_crear)
        nombre.grid(row = 0, column = 2)

        Label(self.ventana_crear, text = "Apellidos: ").grid(row = 1, column = 1)
        apellidos = Entry(self.ventana_crear)
        apellidos.grid(row = 1, column = 2)

        Label(self.ventana_crear, text = "Dirección: ").grid(row = 2, column = 1)
        direccion = Entry(self.ventana_crear)
        direccion.grid(row = 2, column = 2)

        Label(self.ventana_crear, text = "Email: ").grid(row = 3, column = 1)
        email = Entry(self.ventana_crear)
        email.grid(row = 3, column = 2)

        Label(self.ventana_crear, text = "Teléfono: ").grid(row = 4, column = 1)
        telefono = Entry(self.ventana_crear)
        telefono.grid(row = 4, column = 2)

        Button(self.ventana_crear, text = "Guardar", command =lambda: self.agregar_contacto(nombre.get(), apellidos.get(), direccion.get(), email.get(), telefono.get(), UsuarioLogueado())).grid(row = 5, column = 2, sticky = W)
    
        
    # Agregamos el nuevo contacto a la base de datos

    def agregar_contacto(self, nombre, apellidos, direccion, email, telefono,UsuarioLogueado):
        query = "INSERT INTO Contactos ( nombre, apellidos, direccion, email, telefono, creador) VALUES (%s,%s,%s,%s,%s,%s)"          
        parameters = (nombre, apellidos, direccion, email, telefono, UsuarioLogueado)
        cursor.execute(query, parameters)
        conexion.commit()
        
        self.ventana_crear.destroy()
        self.message['text'] = "Contacto guardado satisfactoriamente" 

    # Editando Contactos

    def EditarContacto(self):
        self.ventana_editar = Toplevel() 
        self.ventana_editar.title = "Actualizar Contacto"

        Label(self.ventana_editar, text = 'Nombre: ').grid(row = 0, column = 1)
        nombre = Entry(self.ventana_editar)
        nombre.grid(row = 0, column = 2)
        

        Label(self.ventana_editar, text = "Apellidos: ").grid(row = 1, column = 1)
        apellidos = Entry(self.ventana_editar)
        apellidos.grid(row = 1, column = 2)

        Label(self.ventana_editar, text = "Dirección: ").grid(row = 2, column = 1)
        direccion = Entry(self.ventana_editar)
        direccion.grid(row = 2, column = 2)

        Label(self.ventana_editar, text = "Email: ").grid(row = 3, column = 1)
        email = Entry(self.ventana_editar)
        email.grid(row = 3, column = 2)

        Label(self.ventana_editar, text = "Teléfono: ").grid(row = 4, column = 1)
        telefono = Entry(self.ventana_editar)
        telefono.grid(row = 4, column = 2)

        Label(self.ventana_editar, text = "Id: ").grid(row= 5, column = 1)
        Id = Entry(self.ventana_editar)
        Id.grid(row = 5, column = 2)

        #Botón de busqueda del contacto a editar por nombre y de Actualizar

        Button(self.ventana_editar, text = "Buscar", command = lambda: self.TraerDatos(nombre.get())).grid(row = 0, column = 3, sticky = W + E)
        Button(self.ventana_editar, text = "Actualizar", command = lambda:self.ActualizarContacto(nombre.get(), apellidos.get(), direccion.get(), email.get(), telefono.get(), Id.get(), UsuarioLogueado())).grid(row = 5, column = 3, sticky = W + E)

        # Tabla para mostrar los datos del contacto a editar

        self.tree = ttk.Treeview(self. ventana_editar, height = 4, columns=[f"#{n}" for n in range(0,5)])
        self.tree.grid(row = 6, column = 1, columnspan = 5)
        self.tree.heading('#0', text = "id", anchor = CENTER)
        self.tree.heading('#1', text = "nombre", anchor = CENTER)
        self.tree.heading('#2', text = "apellidos", anchor = CENTER)
        self.tree.heading('#3', text = "dirección", anchor = CENTER)
        self.tree.heading('#4', text = "email", anchor = CENTER)
        self.tree.heading('#5', text = "teléfono", anchor = CENTER)

    # Funcion que ejecuta el botón Actualizar y graba el contacto actualizado

    def ActualizarContacto(self, nombre, apellidos, direccion, email, telefono, Id, UsuarioLogueado):
        query = "UPDATE Contactos SET nombre = %s, apellidos = %s, direccion = %s , email = %s, telefono = %s, creador = %s WHERE nombre = %s AND Id = %s "
        parameters = (nombre, apellidos, direccion, email, telefono, UsuarioLogueado, nombre, Id)
        cursor.execute(query, parameters)
        conexion.commit()
        
        self.ventana_editar.destroy()
        self.message['text'] = "Contacto actualizado satisfactoriamente" 

        
    # Función para traer a la tabla el contacto a editar desde el botón buscar

    def TraerDatos(self, nombre):
        query = " SELECT * FROM Contactos WHERE nombre = '"+nombre+"' "
        contacto = cursor.fetchall()
        cursor.execute(query)
        for row in contacto :
            print(row)
            self.tree.insert("", 0, text = row [0], values = (row [1], row [2], row[3], row[4], row[5]))

    # Función para buscar y eliminar un contacto de la agenda    
           
    def EliminarContacto(self):
        self.ventana_eliminar = Toplevel()
        self.ventana_eliminar.title = "Eliminar Contacto"

        Label(self.ventana_eliminar, text = 'Nombre: ').grid(row = 0, column = 1)
        nombre = Entry(self.ventana_eliminar)
        nombre.grid(row = 0, column = 2)
        Label(self.ventana_eliminar, text = "Id: ").grid(row = 1, column = 1)
        Id = Entry(self.ventana_eliminar)
        Id.grid(row = 1, column = 2)

        Button(self.ventana_eliminar, text = "Buscar", command = lambda:self.TraerDatos(nombre.get())).grid(row = 0, column = 3, sticky = W + E)
        Button(self.ventana_eliminar, text = "Eliminar", command = lambda:self.BorrarContacto(nombre.get(), Id.get())).grid( row = 1, column = 3, sticky = W + E)
        
        # Tabla para visualizar el contacto a eliminar

        self.tree = ttk.Treeview(self.ventana_eliminar, height = 4, columns=[f"#{n}" for n in range(0,5)])
        self.tree.grid(row = 3, column = 1, columnspan = 5)
        self.tree.heading('#0', text = "id", anchor = CENTER)
        self.tree.heading('#1', text = "nombre", anchor = CENTER)
        self.tree.heading('#2', text = "apellidos", anchor = CENTER)
        self.tree.heading('#3', text = "dirección", anchor = CENTER)
        self.tree.heading('#4', text = "email", anchor = CENTER)
        self.tree.heading('#5', text = "teléfono", anchor = CENTER)

        print("Borrado")

    # Ejecución del borrado del contacto al pulsar el boton Eliminar

    def BorrarContacto (self, nombre, Id):
        query = ' DELETE FROM Contactos WHERE nombre = %s AND Id = %s '
        cursor.execute(query)
        conexion.commit()
        
        self.ventana_eliminar.destroy()
        self.message['text'] = "Contacto eliminado satisfactoriamente"

    # Funcion para buscar contactos en la base de datos:

    def BuscarContacto(self):
        
        self.ventana_buscar = Toplevel()
        self.ventana_buscar.title = "Buscar contacto"

        Label(self.ventana_buscar, text = 'Nombre: ').grid(row = 0, column = 1)
        nombre = Entry(self.ventana_buscar)
        nombre.grid(row = 0, column = 2)
        Button(self.ventana_buscar, text = "Buscar", command = lambda : self.TraerDatos(nombre.get())).grid(row = 0, column = 3)
        Button(self.ventana_buscar, text = "Salir", command =self.ventana_buscar.destroy).grid(row = 1, column = 3)

        # Tabla para mostrar los datos del contacto buscado

        self.tree = ttk.Treeview(self.ventana_buscar, height = 4, columns=[f"#{n}" for n in range(0,5)])
        self.tree.grid(row = 3, column = 1, columnspan = 5)
        self.tree.heading('#0', text = "id", anchor = CENTER)
        self.tree.heading('#1', text = "nombre", anchor = CENTER)
        self.tree.heading('#2', text = "apellidos", anchor = CENTER)
        self.tree.heading('#3', text = "dirección", anchor = CENTER)
        self.tree.heading('#4', text = "email", anchor = CENTER)
        self.tree.heading('#5', text = "teléfono", anchor = CENTER)

    def SalirAgenda(self):
        self.master.destroy()

def Mostrar_Menu():
    aplicacion1 = Ventana()



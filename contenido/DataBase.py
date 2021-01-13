import pymysql

def CrearConexion(nombre):
    conexion = pymysql.connect(host = "b6bauoez7gkwtblar05j-mysql.services.clever-cloud.com",
                               user = "ulunmrda6nf0ozil",
                               passwd = "QnXZVdSiZrUF3yLpfthP", 
                               db = "b6bauoez7gkwtblar05j")
    return conexion

def CrearCursor(conexion):
    cursor = conexion.cursor()
    return cursor


def CrearTablaContactos(conexion, cursor):
    query = "CREATE TABLE IF NOT EXISTS Contactos ( id INTEGER, nombre varchar(60), apellidos varchar (255), direccion varchar (255), email varchar (120), telefono varchar (9), PRIMARY KEY (id AUTOINCREMENT))"
    cursor.execute(query)
    conexion.commit()

def CrearTablaUsuarios(conexion, cursor):
    query = "CREATE TABLE IF NOT EXISTS Usuarios ( Id INTEGER, usuario varchar (60), contraseña varchar (60), PRIMARY KEY ( Id AUTOINCREMENT))"
    cursor.execute(query)
    conexion.commit()
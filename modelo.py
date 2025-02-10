
import sqlite3
import re
from datetime import datetime

# Conectar a la base de datos
#### CREO LA CLASE Y CONSTRUCTOR 
def conexion():
    con = sqlite3.connect("mibase.db")  # Cree mi base de datos
    return con  # Retorna el objeto de conexión

# Crear la tabla de mi base
def crear_base():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS mascotas_perdidas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_dueño TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL,
                email TEXT NOT NULL,
                nombre_mascota TEXT NOT NULL,
                color TEXT NOT NULL,
                edad TEXT NOT NULL,
                fecha_perdida TEXT NOT NULL
            )"""

    cursor.execute(sql)
    con.commit()

crear_base()   

# Tomado del ejemplo del profesor
try:
    conexion()
    crear_base()
except Exception as i:
    print("Error al crear la base de datos:", i)


# Función para añadir datos
def añadir_mascota(nombre_dueño,telefono, direccion, email, nombre_mascota, color, edad, fecha, tree): # entre parentesis parametros
    if not validar_campos(var_nombre_dueño, var_telefono, var_direccion, var_email, var_nombre_mascota, var_color, var_edad, var_fecha):
        return
    con = conexion()
    cursor = con.cursor()
    data = (nombre_dueño, telefono, direccion, email, nombre_mascota, color, edad, fecha)  # Todos los campos
    sql = """
    INSERT INTO mascotas_perdidas (nombre_dueño, telefono, direccion, email, nombre_mascota, color, edad, fecha_perdida)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, data)
    con.commit()
    actualizar_treeview(tree)
    messagebox.showinfo("Éxito", "Campos ingresados correctamente")

# Actualizar Treeview tomado de ejemplo
def actualizar_treeview(tree):
    for element in tree.get_children():
        tree.delete(element)

    con = conexion()
    cursor = con.cursor()
    sql = "SELECT * FROM mascotas_perdidas ORDER BY id ASC"
    datos = cursor.execute(sql)
    informacion = datos.fetchall()
    for info in informacion:
        tree.insert("", "end", values=info)


# Función para borrar datos
def borrar_mascota(tree):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione un registro para borrar")
        return

    item = tree.item(seleccion)
    mi_id = item['values'][0]

    con = conexion()
    cursor = con.cursor()
    sql = "DELETE FROM mascotas_perdidas WHERE id=?"
    cursor.execute(sql, (mi_id,))
    con.commit()
    actualizar_treeview(tree)
    messagebox.showinfo("Éxito", "Registro borrado correctamente")


# Función para editar datos
def editar_datos(registro_id, nombre_dueño, telefono, direccion, email, nombre_mascota, color, edad, fecha_perdida, tree):
    if not registro_id:
        messagebox.showerror("Error", "Seleccione un registro para editar")
        return
    if not nombre_dueño or not telefono or not direccion or not email or not nombre_mascota or not color or not edad or not fecha_perdida:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    if not validar_email(email):
        messagebox.showerror("Error", "Formato de email incorrecto")
        return
    if not (nombre_dueño and telefono and direccion and email and nombre_mascota and color and edad and fecha_perdida):
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    con = conexion()
    cursor = con.cursor()
    sql = """UPDATE mascotas_perdidas 
             SET nombre_dueño=?, telefono=?, direccion=?, email=?, nombre_mascota=?, color=?, edad=?, fecha_perdida=?
             WHERE id=?"""
    data = (nombre_dueño, telefono, direccion, email, nombre_mascota, color, edad, fecha_perdida, registro_id)
    cursor.execute(sql, data)
    con.commit()
    actualizar_treeview(tree)
    messagebox.showinfo("Éxito", "Datos actualizados correctamente")

def consultar(tree):
    
    for item in tree.get_children():
        tree.delete(item)
    con = conexion()
    cursor = con.cursor()
    sql = "SELECT * FROM mascotas_perdidas"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

def obtener_id(tree):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione un registro para editar")
        return None
    item = tree.item(seleccion)
    return item['values'][0]
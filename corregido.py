import sqlite3
from tkinter import *
import re
from tkinter import ttk, messagebox
from datetime import datetime

# Conectar a la base de datos
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

# Funcion para validar email y telefono
def validar_telefono(telefono):
    patron = r'^\d{10}$'
    return re.match(patron, telefono)

def validar_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email)
 
def validar_fecha(fecha):
    patron = r'^\d{2}/\d{2}/\d{4}$'
    if not re.match(patron, fecha):
        return False
    try:
        datetime.strptime(fecha, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def validar_campos(var_nombre_dueño, var_telefono, var_direccion, var_email, var_nombre_mascota, var_color, var_edad, var_fecha):
    if not all([var_nombre_dueño.get(), var_telefono.get(), var_direccion.get(), var_email.get(), var_nombre_mascota.get(), var_color.get(), var_edad.get(), var_fecha.get()]):
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return False
    if not validar_telefono(var_telefono.get()):  # Aquí estamos obteniendo el valor con .get()
        messagebox.showerror("Error", "El número de teléfono debe tener 10 dígitos")
        return False
    if not validar_email(var_email.get()):
        messagebox.showerror("Error", "Formato de email incorrecto")
        return False
    if not validar_fecha(var_fecha.get()):
        messagebox.showerror("Error", "Formato de fecha incorrecto. Use dd/mm/yyyy")
        return False
    return True

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

    
#  interfaz gráfica TK
root = Tk()
root.title("Datos titular")
root.configure(bg="violet")

# Hago las etiquetas
titulo = Label(root, text="Base de datos Mascotas Perdidas", bg="DarkOrchid3", fg="thistle1", height=1, width=60,font=("Arial", 16, "bold"))
titulo.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

nombre_dueño = Label(root, text="Nombre del dueño")
nombre_dueño.grid(row=1, column=0, sticky=W)
telefono =Label(root, text="Teléfono")
telefono.grid(row=2, column=0, sticky=W)
direccion = Label(root, text="Dirección")
direccion.grid(row=3, column=0, sticky=W)
email=Label(root, text="Email")
email.grid(row=4, column=0, sticky=W)
nombre_mascota= Label(root,text="Nombre de la mascota")
nombre_mascota.grid(row=5, column= 0,sticky=W)
edad= Label(root, text="Edad" )
edad.grid(row=6, column=0, sticky=W)
color=Label(root,text="Color")
color.grid(row=7,column=0, sticky= W)
fecha= Label(root, text="Fecha en que se perdio")
fecha.grid(row=8, column=0, sticky=W)

# Variables de entrada ESTARA BIEN?
var_nombre_dueño = StringVar()
var_telefono = StringVar()
var_direccion = StringVar()
var_email = StringVar()
var_nombre_mascota = StringVar()
var_edad = StringVar()
var_color = StringVar()
var_fecha = StringVar()

# Entradas tabla titulares
entrada1= Entry(root, textvariable=var_nombre_dueño)
entrada1.grid(row=1, column=1)
entrada2= Entry(root, textvariable=var_telefono)
entrada2.grid(row=2, column=1)
entrada3= Entry(root, textvariable=var_direccion)
entrada3.grid(row=3, column=1)
entrada4= Entry(root, textvariable=var_email)
entrada4.grid(row=4, column=1)
entrada5= Entry(root,textvariable= var_nombre_mascota)
entrada5.grid(row=5, column=1)
entrada6= Entry(root,textvariable=var_edad)
entrada6.grid(row=6, column=1)
entrada7= Entry(root,textvariable=var_color)
entrada7.grid(row=7, column=1)
entrada8 = Entry(root, textvariable=var_fecha)
entrada8.grid(row=8, column=1)

# Entrada tabla mascotas





# Botones Y VARIABLES VAR
Button(root, text="Añadir Mascota", command=lambda: añadir_mascota(
    var_nombre_dueño.get(), var_telefono.get(), var_direccion.get(), var_email.get(), var_nombre_mascota.get(), var_color.get(), var_edad.get(), var_fecha.get(), tree
)).grid(row=13, column=0)

Button(root, text="Borrar Datos", command=lambda: borrar_mascota(tree)).grid(row=14, column=0)

Button(root, text="Editar Datos", command=lambda: editar_datos(obtener_id(tree),
    var_nombre_dueño.get(), var_telefono.get(), var_direccion.get(), var_email.get(),var_nombre_mascota.get(), var_color.get(), var_edad.get(), var_fecha.get(), tree
)).grid(row=15, column=1)

Button(root, text= "Consultar", command=lambda: consultar(tree)).grid(row= 16, column=1)

# Treeview
tree = ttk.Treeview(root, columns=("ID", "Nombre_dueño", "Teléfono", "Dirección", "Email","Nombre_mascota", "Color", "Edad", "Fecha_perdida"), show="headings")
columns = [("ID", "ID"), ("Nombre_dueño", "Nombre_dueño"), ("Teléfono", "Teléfono"), ("Dirección", "Dirección"), ("Email", "Email"), ("Nombre_mascota", "Nombre_mascota"), ("Color", "Color"), ("Edad", "Edad"), ("Fecha_perdida", "Fecha_perdida")]

for col, text in columns: 
    tree.heading(col, text=text)

column_widths = {"ID": 20, "Nombre_dueño": 150, "Teléfono": 100, "Dirección": 150, "Email": 150, "Nombre_mascota": 150, "Color": 100, "Edad": 100, "Fecha_perdida": 100} 
for col, width in column_widths.items(): 
    tree.column(col, width=width)
tree.grid(row=12, column=0, columnspan=4)

tree.heading("ID", text="ID")
tree.heading("Nombre_dueño", text="Nombre_dueño")
tree.heading("Teléfono", text="Teléfono")
tree.heading("Dirección", text="Dirección")
tree.heading("Email", text="Email")
tree.heading("Nombre_mascota", text="Nombre_mascota")
tree.heading("Color", text= "Color")
tree.heading("Edad", text= "Edad")
tree.heading("Fecha_perdida", text="Fecha_perdida")

actualizar_treeview(tree)

# Iniciar la aplicación
root.mainloop()

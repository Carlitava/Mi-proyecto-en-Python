"""
Módulo modelo.py

Este módulo maneja la conexión a la base de datos y las operaciones CRUD
para la tabla `mascotas_perdidas`.
"""

import sqlite3
from validar import Validate


class Abmc:
    """

    Clase para manejar la base de datos y realizar operaciones CRUD
    sobre la tabla `mascotas_perdidas`.
    """

    def __init__(self):
        """
        Constructor de la clase Abmc.
        Establece la conexión con la base de datos y la crea si no existe.
        """
        try:
            self.conexion()
            self.crear_base()
        except Exception as i:
            print("Error al crear la base de datos:", i)
        self.obj_regex = Validate()

    def conexion(self):
        """
        Establece la conexión con la base de datos SQLite.
        :return: Objeto de conexión a la base de datos.
        """
        con = sqlite3.connect("mibase.db")  
        return con  

    def crear_base(self):
        """
        Crea la tabla `mascotas_perdidas` si no existe en la base de datos.
        """
        con = self.conexion()
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

    def añadir_mascota(self, nombre_dueño, telefono, direccion,
                       email, nombre_mascota, color, edad, fecha):
        """
        Añade una nueva mascota a la base de datos.

        :param nombre_dueño: Nombre del dueño.
        :param telefono: Teléfono del dueño.
        :param direccion: Dirección del dueño.
        :param email: Correo electrónico del dueño.
        :param nombre_mascota: Nombre de la mascota.
        :param color: Color de la mascota.
        :param edad: Edad de la mascota.
        :param fecha: Fecha de pérdida de la mascota.
        :return: Mensaje de éxito o error.
        """
        if not (
                nombre_dueño and telefono and direccion and email and nombre_mascota and color and edad and fecha):
            return "Error: Todos los campos son obligatorios"
        if not self.obj_regex.regex_email(email):
            return "Error: Formato de email incorrecto."
        if not self.obj_regex.regex_telefono(telefono):
            return "Error: Formato de teléfono incorrecto (solo números, 8-15 dígitos)."
        if not self.obj_regex.regex_fecha(fecha):
            return "Error: Formato de fecha incorrecto (YYYY-MM-DD)."

        con = self.conexion()
        cursor = con.cursor()
        data = (
            nombre_dueño,
            telefono,
            direccion,
            email,
            nombre_mascota,
            color,
            edad,
            fecha)
        sql = """INSERT INTO mascotas_perdidas
                 (nombre_dueño, telefono, direccion, email, nombre_mascota, color, edad, fecha_perdida)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

        cursor.execute(sql, data)
        con.commit()
        print("Datos ingresados")
        return "Datos ingresados correctamente"

# Actualizar Treeview
    def tree_modelo(self):
        """
        Obtiene todos los registros de la tabla `mascotas_perdidas`.

        :return: Lista de tuplas con los registros de la tabla.
        """
        con = self.conexion()
        cursor = con.cursor()
        sql = "SELECT * FROM mascotas_perdidas ORDER BY id ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        return datos

    def borrar_mascota(self, id_mascota):
        """
        Borra una mascota de la base de datos según su ID.

        :param id_mascota: ID de la mascota a eliminar.
        :return: Mensaje de éxito o error.
        """
        if not id_mascota:
            return "Error: Seleccione un registro para borrar"

        try:
            con = self.conexion()
            cursor = con.cursor()
            print(f"Intentado borrar ID: {id_mascota}")
            sql = "DELETE FROM mascotas_perdidas WHERE id=?"
            cursor.execute(sql, (id_mascota,))
            con.commit()

            if cursor.rowcount == 0:
                print("Error: El ID no existe en la base de datos")
                return "Error: El registro no existe en la base de datos"
            print("✅ Registro eliminado correctamente")
            return "Éxito: Registro borrado correctamente"
        except Exception as e:
            print(f"Error al borrar: {e}")
            return f"Error:{e}"

    def verificar_email(self, email):
        """Verifica si el email tiene un formato válido."""
        if not self.obj_regex.regex_email(email):
            return "Error: Formato de email incorrecto."
        return "Éxito: Email valido"


    def editar_datos(self, registro_id, nombre_dueño, telefono, direccion,
                     email, nombre_mascota, color, edad, fecha_perdida):
        """
        Edita los datos de una mascota en la base de datos.
        :param registro_id: ID de la mascota a editar.
        :param nombre_dueño: Nombre del dueño.
        :param telefono: Teléfono del dueño.
        :param direccion: Dirección del dueño.
        :param email: Correo electrónico del dueño.
        :param nombre_mascota: Nombre de la mascota.
        :param color: Color de la mascota.
        :param edad: Edad de la mascota.
        :param fecha_perdida: Fecha de pérdida de la mascota.
        :return: Mensaje de éxito o error.
        """
        if not registro_id:
            return "Error", "Seleccione un registro para editar"

        if not (nombre_dueño and telefono and direccion and email and nombre_mascota and color and edad and fecha_perdida):
            return "Error", "Todos los campos son obligatorios"
            # Validaciones antes de actualizar
        if not self.obj_regex.regex_email(email):
            return "Error: Formato de email incorrecto."

        if not self.obj_regex.regex_telefono(telefono):
            return "Error: Formato de teléfono incorrecto."

        if not self.obj_regex.regex_fecha(fecha_perdida):
            return "Error: Formato de fecha incorrecto."

        con = self.conexion()
        cursor = con.cursor()
        sql = """UPDATE mascotas_perdidas
             SET nombre_dueño=?, telefono=?, direccion=?, email=?, nombre_mascota=?, color=?, edad=?, fecha_perdida=?
             WHERE id=?"""
        data = (
            nombre_dueño,
            telefono,
            direccion,
            email,
            nombre_mascota,
            color,
            edad,
            fecha_perdida,
            registro_id)
        cursor.execute(sql, data)
        con.commit()
        con.close()
        return "Éxito", "Registro seleccionado porfavor edite y añada correctamente"
    def obtener_mascota(self, id_mascota):
        """
        Obtiene los datos de una mascota en la base de datos.
    
        :param id_mascota: ID de la mascota que se desea obtener.
        :return: Una tupla con los datos de la mascota o None si no se encuentra.
        """
        con = self.conexion()
        cursor = con.cursor()
        sql = "SELECT * FROM mascotas_perdidas WHERE id = ?"
        cursor.execute(sql, (id_mascota,))
        datos = cursor.fetchone()  # Usamos fetchone() porque estamos buscando un solo registro

        if datos:
            return datos  # Retorna todos los datos de la mascota como una tupla
        else:
            return None  # Retorna None si no se encontró la mascota

    def consultar(self):
        """
        Obtiene todos los registros de la tabla `mascotas_perdidas`.

        :return: Lista de tuplas con los registros.
        """
        con = self.conexion()
        cursor = con.cursor()
        sql = "SELECT * FROM mascotas_perdidas"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def obtener_id(self, tree):
        """
        Obtiene el ID del registro seleccionado en el Treeview.

        :param tree: Treeview donde se selecciona el registro.
        :return: ID del registro seleccionado o None si no hay selección.
        """
        seleccion = tree.selection()
        if not seleccion:
            return None
        
        item = tree.item(seleccion)
        return item['values'][0]
        

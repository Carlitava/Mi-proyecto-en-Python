"""
Módulo vista.py

Este módulo maneja la interfaz gráfica de usuario (GUI) para la aplicación de
gestión de mascotas perdidas utilizando Tkinter.
"""
from tkinter import *
from tkinter import ttk, messagebox
from modelo import Abmc
from logger import Logger 
import os
import sys
import subprocess
import threading
from pathlib import Path


class Vista():
    """
    Clase que maneja la interfaz gráfica de la aplicación.

    Permite al usuario ingresar, modificar y eliminar datos sobre mascotas perdidas.
    """

    def __init__(self, root):
        """
        Constructor de la clase Vista.

        :param root: Ventana principal de Tkinter.
        """
        self.obj_abmc = Abmc()
        self.logger = Logger()
        self.obj_abmc.agregar_observador(self.logger)
        self.root = root
        self.root.title("Datos titular")
        self.root.configure(bg="violet")
        self.theproc = None
        self.raiz = Path(__file__).resolve().parent
        self.ruta_server = os.path.join(self.raiz, 'src', 'servidor', 'udp_server.py')

        
        
# ETIQUETAS
        self.titulo = Label(
            self.root,
            text="Base de datos Mascotas Perdidas",
            bg="DarkOrchid3",
            fg="thistle1",
            height=1,
            width=60,
            font=("Arial", 16,"bold")
        )
        self.titulo.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.nombre_dueño = Label(self.root, text="Nombre del dueño")
        self.nombre_dueño.grid(row=1, column=0, sticky=W)
        self.telefono = Label(self.root, text="Teléfono")
        self.telefono.grid(row=2, column=0, sticky=W)
        self.direccion = Label(self.root, text="Dirección")
        self.direccion.grid(row=3, column=0, sticky=W)
        self.email = Label(self.root, text="Email")
        self.email.grid(row=4, column=0, sticky=W)
        self.nombre_mascota = Label(self.root, text="Nombre de la mascota")
        self.nombre_mascota.grid(row=5, column=0, sticky=W)
        self.edad = Label(self.root, text="Edad")
        self.edad.grid(row=6, column=0, sticky=W)
        self.color = Label(self.root, text="Color")
        self.color.grid(row=7, column=0, sticky=W)
        self.fecha = Label(self.root, text="Fecha en que se perdio")
        self.fecha.grid(row=8, column=0, sticky=W)

# Variables de entrada 
        self.var_nombre_dueño = StringVar()
        self.var_telefono = StringVar()
        self.var_direccion = StringVar()
        self.var_email = StringVar()
        self.var_nombre_mascota = StringVar()
        self.var_edad = StringVar()
        self.var_color = StringVar()
        self.var_fecha = StringVar()

# Entradas
        self.entrada1 = Entry(self.root, textvariable=self.var_nombre_dueño)
        self.entrada1.grid(row=1, column=1)
        self.entrada2 = Entry(self.root, textvariable=self.var_telefono)
        self.entrada2.grid(row=2, column=1)
        self.entrada3 = Entry(self.root, textvariable=self.var_direccion)
        self.entrada3.grid(row=3, column=1)
        self.entrada4 = Entry(self.root, textvariable=self.var_email)
        self.entrada4.grid(row=4, column=1)
        self.entrada5 = Entry(self.root, textvariable=self.var_nombre_mascota)
        self.entrada5.grid(row=5, column=1)
        self.entrada6 = Entry(self.root, textvariable=self.var_edad)
        self.entrada6.grid(row=6, column=1)
        self.entrada7 = Entry(self.root, textvariable=self.var_color)
        self.entrada7.grid(row=7, column=1)
        self.entrada8 = Entry(self.root, textvariable=self.var_fecha)
        self.entrada8.grid(row=8, column=1)

# Treeview
        self.tree = ttk.Treeview(
            root,
            columns=(
                "ID",
                "Nombre_dueño",
                "Teléfono",
                "Dirección",
                "Email",
                "Nombre_mascota",
                "Color",
                "Edad",
                "Fecha_perdida"),
            show="headings")
        columns = [
            ("ID",
             "ID"),
            ("Nombre_dueño",
             "Nombre_dueño"),
            ("Teléfono",
             "Teléfono"),
            ("Dirección",
              "Dirección"),
            ("Email",
              "Email"),
            ("Nombre_mascota",
              "Nombre_mascota"),
            ("Color",
              "Color"),
            ("Edad",
            "Edad"),
            ("Fecha_perdida",
              "Fecha_perdida")]

        for col, text in columns:
          self.tree.heading(col, text=text)


        column_widths = {
            "ID": 20,
            "Nombre_dueño": 150,
            "Teléfono": 100,
            "Dirección": 150,
            "Email": 150,
            "Nombre_mascota": 150,
            "Color": 100,
            "Edad": 100,
            "Fecha_perdida": 100}
        for col, width in column_widths.items():
            self.tree.column(col, width=width)
        self.tree.grid(row=12, column=0, columnspan=4)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre_dueño", text="Nombre_dueño")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Nombre_mascota", text="Nombre_mascota")
        self.tree.heading("Color", text="Color")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Fecha_perdida", text="Fecha_perdida")


# Botones Y VARIABLES VAR
        self.boton_alta = Button(self.root, text="Añadir Mascota", command=lambda: self.alta_vista(
            self.var_nombre_dueño, self.var_telefono, self.var_direccion, self.var_email, self.var_nombre_mascota, self.var_color, self.var_edad, self.var_fecha, self.tree
        )).grid(row=13, column=0)

        self.boton_borrar = Button(
            self.root,
            text="Borrar Datos",
            command=lambda: self.obj_abmc.borrar_mascota(
                self.obtener_id(
                    self.tree))).grid(
            row=14,
            column=0)

        self.boton_editar = Button(
            self.root, text="Editar Datos",
            command=lambda: self.editar_mascota()).grid(row=15, column=1)

        self.boton_consultar = Button(
            self.root,
            text="Consultar",
            command=lambda: self.actualizar_treeview(
                self.tree)).grid(
            row=16,
            column=1)
        
        self.boton_prender = Button(self.root, text="Prender Servidor UDP", command=self.prender_servidor)
        self.boton_prender.grid(row=17, column=0)

        self.boton_apagar = Button(self.root, text="Apagar Servidor UDP", command=self.apagar_servidor)
        self.boton_apagar.grid(row=17, column=1)

# FUNCIONES AUXILIARES

    def obtener_id(self, tree):
        """
        Obtiene el ID de la mascota seleccionada en el Treeview.

        :return: ID de la mascota seleccionada o None si no hay selección.
        """
        seleccion = tree.selection()  # Obtiene la fila seleccionada
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un registro para borrar")
            return None

        # Obtiene los datos de la fila seleccionada
        item = tree.item(seleccion)
        id_mascota = item['values'][0]  # Retorna el ID (primer valor)
        print(f"ID obtenido: {id_mascota}")  # 🔍 Depuración
        return id_mascota

    def borrar_mascota(self):
        """
        Borra la mascota seleccionada de la base de datos.
        """
        id_mascota = self.obtener_id(self.tree)  # Llama a obtener_id()
        print(f"ID seleccionado para borrar: {id_mascota}")
        if id_mascota:  # Si hay un ID seleccionado
            resultado = self.obj_abmc.borrar_mascota(id_mascota)
           
            if "Error" in resultado:
                messagebox.showerror("Error", resultado)
            else:
                messagebox.showinfo("Exito", "Registro borrado.")
            self.actualizar_treeview(self.tree)
        else:
            print("No se selecciono un ID")
            messagebox.showerror(
                "Error", "Debe seleccionar un registro para borrar.")

    def alta_vista(self, nombre_dueño, telefono, direccion,
                  email, nombre_mascota, color, edad, fecha, tree):
        """
        Registra una nueva mascota en la base de datos o edita una existente.

        Si un ID está seleccionado, actualiza el registro en lugar de crear uno nuevo.
        """
        view = self.obj_abmc.añadir_mascota(
            nombre_dueño.get(), telefono.get(), direccion.get(), email.get(), nombre_mascota.get(), color.get(), edad.get(), fecha.get())
        if "Error" in view:  # Si hay un error, mostramos un mensaje de error
            messagebox.showerror("Error", view)
        else:
            messagebox.showinfo("Éxito", view)
            self.actualizar_treeview()
        if view [0] == "ok":
            self.actualizar_treeview()
            nombre_dueño.set("")
            telefono.set("")
            direccion.set("")
            email.set("")
            nombre_mascota.set("")
            color.set("")
            edad.set("")
            fecha.set("")
         #else: pass
    ######
    
    def editar_mascota(self,):
        """
        Carga los datos de la mascota seleccionada en los campos de entrada para edición.

        Permite modificar los datos y luego guardar los cambios con el botón "Editar Mascota".
        """
        id_mascota = self.obtener_id(self.tree)  # Obtener ID seleccionado
        if id_mascota is None:
           messagebox.showerror("Error", "Debe seleccionar un registro para editar.")
           return
        
        datos_mascota = self.obj_abmc.obtener_mascota(id_mascota)
        if not datos_mascota:
           messagebox.showerror("Error", "No se pudo obtener los datos de la mascota.")
           return

        resultado = self.obj_abmc.editar_datos(
            id_mascota,
            self.var_nombre_dueño.get(), self.var_telefono.get(),
            self.var_direccion.get(), self.var_email.get(),
            self.var_nombre_mascota.get(), self.var_color.get(),
            self.var_edad.get(), self.var_fecha.get()
        )

        if "Error" in resultado:
            messagebox.showerror("Error", resultado)
        else:
            messagebox.showinfo("Éxito", resultado)
            self.actualizar_treeview()

    def actualizar_treeview(self):
        """
        Actualiza el Treeview con los datos más recientes de la base de datos.
        """
        for element in self.tree.get_children():
            self.tree.delete(element)

        datos = self.obj_abmc.tree_modelo()

        # informacion = datos.fetchall()
        for info in datos:
            self.tree.insert("", "end", values=info)
    
    def prender_servidor(self):
        if self.theproc:
            print("El servidor ya está corriendo.")
            return
        ruta = self.ruta_server
        if os.path.exists(ruta):
            def lanzar():
                self.theproc = subprocess.Popen([sys.executable, ruta])
                self.theproc.communicate()
            threading.Thread(target=lanzar, daemon=True).start()
            print(" Servidor UDP iniciado.")
        else:
            print(" No se encontró el archivo del servidor UDP.")

    def apagar_servidor(self):
        if self.theproc:
            self.theproc.kill()
            self.theproc = None
            print("Servidor UDP detenido.")
        else:
            print("No hay servidor corriendo.")

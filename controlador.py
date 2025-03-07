"""
controlador.py

Este módulo actúa como el punto de entrada principal de la aplicación.

Se encarga de:
- Crear la ventana principal de Tkinter.
- Instanciar la clase `Vista`, que gestiona la interfaz gráfica.
- Ejecutar el bucle principal de la aplicación.

Uso:
    Ejecutar este script para iniciar la aplicación.
"""
from tkinter import *
from vista import Vista

if __name__ == "__main__":
    """
    Punto de entrada de la aplicación.

    Se crea una ventana principal de Tkinter y se instancia la clase Vista.
    Luego, se inicia el bucle principal de la interfaz gráfica.
    """
    ventana = Tk()
    obj = Vista(ventana)
    ventana.mainloop()

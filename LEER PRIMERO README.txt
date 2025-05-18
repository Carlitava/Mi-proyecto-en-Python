Proyecto final Mascotas Perdidas:

!!!!Como ejecutar la aplicacion:

1. Requisitos Python 3.x
2. Desde terminal ubicarse en la carpeta del proyecto
3. Ejecutar: Python controlador.py

Esto abrira la interfaz principal para que ingrese sus datos y los de su mascota.

## Función de los botones

Prender Servidor UDP**: Lanza `udp_server.py`, que registra los mensajes entrantes en `src/servidor/registro.txt`.
Apagar Servidor UDP**: Detiene el servidor.

---
 Registro de Logs

registro.log: generado con el patrón observador.
registro.txt: generado por el servidor UDP al recibir mensajes.

---
 Clientes UDP

- cliente_str.py: envía mensajes de texto.
- cliente_hex.py: envía datos en hexadecimal.

Puedes ejecutarlos desde terminal para probar comunicación con el servidor UDP.

---

Base de Datos

- mibase.db: contiene los registros ingresados desde la app.


📌 Instrucciones para ver la documentación 📌

Para ver la documentación generada con Sphinx, abra el siguiente archivo en un navegador:

📂 docs/_build/html/index.html

Pasos:
1. Descomprimir el archivo ZIP.
2. Ir a la carpeta `docs/_build/html/`.
3. Hacer doble clic en `index.html` para abrir la documentación en un navegador.

📌 Si tiene problemas, puede abrir manualmente el archivo `index.html` en Chrome, Edge o Firefox.
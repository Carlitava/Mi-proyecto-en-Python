import socketserver
import socket
import binascii
from datetime import datetime
import os

#global Host
def guardar_log(mensaje, direccion_ip):
    with open("registro.txt", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {direccion_ip} - {mensaje}\n")

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("Hola 1")
        data = self.request[0].strip()
        socket = self.request[1]

        try:
            mensaje = data.decode("utf-8")
            print("Mensaje recibido como STRING:", mensaje)
            guardar_log(mensaje, self.client_address[0])
        except UnicodeDecodeError:
            mensaje_hex = binascii.hexlify(data).decode("utd-8")
            print("Mensaje recibido como HEXADECIMAL:", mensaje_hex)
            guardar_log(mensaje_hex, self.client_address[0])

        value2 = 0xA0
        packed_data_2 = bytearray()
        packed_data_2 += value2.to_bytes(1, "big")
        socket.sendto(packed_data_2, self.client_address)
        print("--2--")

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        print(f"Servidor UDP corriendo en {HOST}:{PORT}...")
        server.serve_forever()


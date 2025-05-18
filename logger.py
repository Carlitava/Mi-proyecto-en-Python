from observador import Observador

class Logger(Observador):
    def update(self, sujeto):
        with open("registro.log", "a") as archivo:
            archivo.write(f"Estado actualizado:{sujeto.get_estado()}\n")




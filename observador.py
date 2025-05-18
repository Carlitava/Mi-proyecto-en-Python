class Subject:
    def __init__(self):
        self._estado = None
        self._observadores= []

    def agregar_observador(self, observador):
        self._observadores.append(observador)
        
    def borrar_observador(self, observador):
        self._observadores.remove(observador)

    def notificar(self):
        for observador in self._observadores:
            observador.update(self)
        
    def set_estado(self,nuevo_estado):
        self._estado = nuevo_estado
        self.notificar()
        
    def get_estado(self):
        return self._estado

class Observador:
    def update(self, sujeto):
        print(f"Observador notificado. Nuevo Estado:{sujeto.get_estado()}")
        
        




"""
Validar.py

Este módulo contiene la clase `Validate`, que proporciona métodos para validar 
entradas de usuario utilizando expresiones regulares. 

Incluye validaciones para:
- Correos electrónicos (`regex_email`).
- Números de teléfono (`regex_telefono`).
- Fechas en formato `YYYY-MM-DD` (`regex_fecha`).
"""
import re


class Validate():
    """Clase para validar entradas de usuario con expresiones regulares."""

    def __init__(self, ):
        pass

    def regex_email(self, email):
        """Verifica si el email tiene un formato válido."""
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email) is not None

    def regex_telefono(self, telefono):
        """Verifica si el teléfono tiene solo números y entre 8-15 dígitos."""
        patron = r'^\d{8,15}$'
        return re.match(patron, telefono) is not None

    def regex_fecha(self, fecha):
        """Verifica si la fecha tiene formato YYYY-MM-DD."""
        patron = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(patron, fecha) is not None

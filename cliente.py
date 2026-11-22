# ==================================================================
# ARCHIVO: cliente.py
# DESCRIPCION: Clase Cliente con validaciones robustas y
# encapsulacion de datos personales.
# ==================================================================

import re
from entidad import Entidad
from excepciones import ClienteError, DatosInvalidosError
from logger import Logger


class Cliente(Entidad):
    """
    CLASE: Cliente

    Representa un cliente de Software FJ.
    Incluye validaciones robustas para:
      - Cedula (10 digitos numericos)
      - Nombre (solo letras, minimo 3 caracteres)
      - Email (formato valido)
      - Telefono (10 digitos)

    PRINCIPIO: Encapsulacion
      - Atributos privados con getters y setters validados
    """

    # Expresiones regulares para validacion
    REGEX_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    REGEX_NOMBRE = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'

    def __init__(self, cedula: str, nombre: str, email: str, telefono: str):
        """
        Constructor de Cliente.
        Valida todos los datos antes de asignarlos.

        Args:
            cedula (str): Cedula del cliente (10 digitos).
            nombre (str): Nombre completo del cliente.
            email (str): Correo electronico.
            telefono (str): Numero de telefono (10 digitos).
        """
        super().__init__()

        # Usar setters que validan automaticamente
        self.cedula = cedula
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self._activo = True

        Logger.info(f"Cliente creado: {self.nombre} (ID: {self.id})")

    # ------------------------------------------------------------------
    # PROPIEDADES CON ENCAPSULACION (Getters y Setters validados)
    # ------------------------------------------------------------------

    @property
    def cedula(self) -> str:
        """Getter de la cedula."""
        return self._cedula

    @cedula.setter
    def cedula(self, valor: str):
        """
        Setter de la cedula con validacion.
        Debe ser exactamente 10 digitos numericos.
        """
        valor = str(valor).strip()
        if not valor.isdigit():
            raise ClienteError(
                f"La cedula '{valor}' contiene caracteres no numericos",
                "CLI-001"
            )
        if len(valor) != 10:
            raise ClienteError(
                f"La cedula debe tener 10 digitos, se recibieron {len(valor)}",
                "CLI-002"
            )
        self._cedula = valor

    @property
    def nombre(self) -> str:
        """Getter del nombre."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        """
        Setter del nombre con validacion.
        Solo letras y espacios, minimo 3 caracteres.
        """
        valor = str(valor).strip()
        if len(valor) < 3:
            raise ClienteError(
                f"El nombre debe tener al menos 3 caracteres",
                "CLI-003"
            )
        if not re.match(self.REGEX_NOMBRE, valor):
            raise ClienteError(
                f"El nombre '{valor}' contiene caracteres no permitidos",
                "CLI-004"
            )
        self._nombre = valor.title()

    @property
    def email(self) -> str:
        """Getter del email."""
        return self._email

    @email.setter
    def email(self, valor: str):
        """
        Setter del email con validacion de formato.
        """
        valor = str(valor).strip().lower()
        if not re.match(self.REGEX_EMAIL, valor):
            raise ClienteError(
                f"El email '{valor}' no tiene un formato valido",
                "CLI-005"
            )
        self._email = valor

    @property
    def telefono(self) -> str:
        """Getter del telefono."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        """
        Setter del telefono con validacion.
        Debe ser exactamente 10 digitos numericos.
        """
        valor = str(valor).strip()
        if not valor.isdigit():
            raise ClienteError(
                f"El telefono '{valor}' contiene caracteres no numericos",
                "CLI-006"
            )
        if len(valor) != 10:
            raise ClienteError(
                f"El telefono debe tener 10 digitos, se recibieron {len(valor)}",
                "CLI-007"
            )
        self._telefono = valor

    @property
    def activo(self) -> bool:
        """Getter del estado activo."""
        return self._activo

    def desactivar(self):
        """Desactiva el cliente."""
        self._activo = False
        Logger.warning(f"Cliente desactivado: {self.nombre}")

    # ------------------------------------------------------------------
    # METODOS IMPLEMENTADOS DE LA CLASE ABSTRACTA
    # ------------------------------------------------------------------

    def obtener_info(self) -> str:
        """
        Devuelve la informacion del cliente en formato legible.
        Implementacion del metodo abstracto de Entidad.
        """
        estado = "Activo" if self._activo else "Inactivo"
        return (f"Cliente: {self.nombre} | Cedula: {self.cedula} | "
                f"Email: {self.email} | Tel: {self.telefono} | {estado}")

    def validar(self) -> bool:
        """
        Valida que todos los datos del cliente sean correctos.
        Retorna True si es valido, False en caso contrario.
        """
        try:
            # Re-validar todos los campos
            self.cedula = self._cedula
            self.nombre = self._nombre
            self.email = self._email
            self.telefono = self._telefono
            return True
        except ClienteError:
            return False

    def __repr__(self) -> str:
        """Representacion para debugging."""
        return f"Cliente(cedula='{self.cedula}', nombre='{self.nombre}')" 

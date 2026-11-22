# ==================================================================
# ARCHIVO: entidad.py
# DESCRIPCION: Clase abstracta base que representa entidades
# generales del sistema. Todas las clases principales (Cliente,
# Servicio, Reserva) heredan de esta clase.
# ==================================================================

from abc import ABC, abstractmethod
from datetime import datetime
import uuid


class Entidad(ABC):
    """
    CLASE ABSTRACTA: Entidad

    Representa una entidad generica del sistema. Proporciona:
    - ID unico generado automaticamente
    - Fecha de creacion
    - Metodos abstractos que deben implementar las clases hijas

    PRINCIPIO: Abstraccion
      - Define la estructura comun sin implementar detalles
    """

    def __init__(self):
        """
        Constructor de la clase Entidad.
        Genera un ID unico y registra la fecha de creacion.
        """
        self._id = str(uuid.uuid4())[:8]  # ID unico de 8 caracteres
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        """Getter del ID (encapsulacion)."""
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        """Getter de la fecha de creacion (encapsulacion)."""
        return self._fecha_creacion

    @abstractmethod
    def obtener_info(self) -> str:
        """
        METODO ABSTRACTO: obtener_info
        Cada clase hija DEBE implementar este metodo para
        devolver su informacion en formato de texto.

        PRINCIPIO: Polimorfismo
          - Cada entidad tiene su propia forma de mostrarse
        """
        pass

    @abstractmethod
    def validar(self) -> bool:
        """
        METODO ABSTRACTO: validar
        Cada clase hija DEBE implementar validaciones
        especificas para sus datos.
        """
        pass

    def __str__(self) -> str:
        """Representacion en string de la entidad."""
        return self.obtener_info()

    def __eq__(self, other) -> bool:
        """Comparacion por ID."""
        if isinstance(other, Entidad):
            return self._id == other._id
        return False

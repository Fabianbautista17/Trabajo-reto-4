# ==================================================================
# ARCHIVO: servicio.py
# DESCRIPCION: Clase abstracta Servicio que define la estructura
# base para todos los servicios de Software FJ.
# ==================================================================

from abc import abstractmethod
from entidad import Entidad
from excepciones import ServicioError


class Servicio(Entidad):
    """
    CLASE ABSTRACTA: Servicio

    Representa un servicio generico de Software FJ.
    Las clases hijas deben implementar:
      - calcular_costo()    -> con sobrecarga
      - describir_servicio() -> descripcion especifica
      - validar()           -> validaciones propias

    PRINCIPIO: Herencia y Polimorfismo
      - Cada servicio especializado hereda y sobrescribe
    """

    def __init__(self, nombre: str, precio_base: float, disponible: bool = True):
        """
        Constructor de Servicio.

        Args:
            nombre (str): Nombre del servicio.
            precio_base (float): Precio base del servicio.
            disponible (bool): Si el servicio esta disponible.
        """
        super().__init__()

        if not nombre or len(nombre.strip()) < 3:
            raise ServicioError(
                "El nombre del servicio debe tener al menos 3 caracteres",
                "SER-001"
            )

        if precio_base <= 0:
            raise ServicioError(
                f"El precio base debe ser positivo, se recibio {precio_base}",
                "SER-002"
            )

        self._nombre = nombre.strip()
        self._precio_base = precio_base
        self._disponible = disponible

    @property
    def nombre(self) -> str:
        """Getter del nombre."""
        return self._nombre

    @property
    def precio_base(self) -> float:
        """Getter del precio base."""
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: float):
        """Setter del precio base con validacion."""
        if valor <= 0:
            raise ServicioError(
                f"El precio debe ser positivo, se recibio {valor}",
                "SER-003"
            )
        self._precio_base = valor

    @property
    def disponible(self) -> bool:
        """Getter de disponibilidad."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        """Setter de disponibilidad."""
        self._disponible = bool(valor)

    # ------------------------------------------------------------------
    # METODOS ABSTRACTOS (deben ser implementados por las hijas)
    # ------------------------------------------------------------------

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """
        METODO ABSTRACTO: calcular_costo

        SOBRECARGA SIMULADA: Cada clase hija implementa
        diferentes variantes del calculo:
          - Con impuestos
          - Con descuentos
          - Con parametros opcionales
        """
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """
        METODO ABSTRACTO: describir_servicio
        Cada servicio tiene su propia descripcion detallada.
        """
        pass

    def obtener_info(self) -> str:
        """Informacion basica del servicio."""
        estado = "Disponible" if self._disponible else "No disponible"
        return (f"Servicio: {self.nombre} | Precio base: ${self._precio_base:.2f} | {estado}") 

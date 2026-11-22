# ==================================================================
# ARCHIVO: servicios.py
# DESCRIPCION: Implementacion de los 3 servicios especializados
# de Software FJ: Reserva de Salas, Alquiler de Equipos y
# Asesorias Especializadas. Cada uno sobrescribe los metodos
# abstractos de la clase Servicio.
# ==================================================================

from servicio import Servicio
from excepciones import ServicioError, DatosInvalidosError
from logger import Logger


# ==================================================================
# SERVICIO 1: Reserva de Salas
# ==================================================================
class ReservaSala(Servicio):
    """
    SERVICIO: Reserva de Salas

    Permite reservar salas de reuniones con diferentes
    capacidades y equipos. El costo varia segun:
      - Horas de reserva
      - Tipo de sala (basica, ejecutiva, auditorio)
      - Impuestos y descuentos
    """

    TIPOS_SALA = {
        "basica": 1.0,
        "ejecutiva": 1.5,
        "auditorio": 2.5
    }

    def __init__(self, nombre: str, precio_base: float,
                 capacidad: int, tipo_sala: str = "basica"):
        """
        Constructor de ReservaSala.

        Args:
            nombre (str): Nombre de la sala.
            precio_base (float): Precio por hora.
            capacidad (int): Capacidad maxima de personas.
            tipo_sala (str): Tipo de sala (basica, ejecutiva, auditorio).
        """
        super().__init__(nombre, precio_base)

        if capacidad <= 0:
            raise ServicioError(
                f"La capacidad debe ser positiva, se recibio {capacidad}",
                "SER-010"
            )

        tipo_sala = tipo_sala.lower()
        if tipo_sala not in self.TIPOS_SALA:
            raise ServicioError(
                f"Tipo de sala '{tipo_sala}' no valido. "
                f"Opciones: {list(self.TIPOS_SALA.keys())}",
                "SER-011"
            )

        self._capacidad = capacidad
        self._tipo_sala = tipo_sala

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @property
    def tipo_sala(self) -> str:
        return self._tipo_sala

    def calcular_costo(self, horas: float, aplicar_impuesto: bool = False,
                       descuento: float = 0.0) -> float:
        """
        SOBRECARGA: calcular_costo

        Variantes de uso:
          - calcular_costo(horas)
          - calcular_costo(horas, aplicar_impuesto=True)
          - calcular_costo(horas, True, descuento=10.0)

        Formula:
          costo = precio_base x horas x factor_tipo
          Si aplica impuesto: costo x 1.19 (IVA 19%)
          Si hay descuento: costo x (1 - descuento/100)
        """
        if horas <= 0:
            raise DatosInvalidosError(
                f"Las horas deben ser positivas, se recibio {horas}",
                "DAT-010"
            )

        if descuento < 0 or descuento > 100:
            raise DatosInvalidosError(
                f"El descuento debe estar entre 0 y 100, se recibio {descuento}",
                "DAT-011"
            )

        factor_tipo = self.TIPOS_SALA[self._tipo_sala]
        costo = self._precio_base * horas * factor_tipo

        if aplicar_impuesto:
            costo *= 1.19  # IVA 19%
            Logger.info(f"Impuesto (19%) aplicado a sala {self.nombre}")

        if descuento > 0:
            costo *= (1 - descuento / 100)
            Logger.info(f"Descuento {descuento}% aplicado a sala {self.nombre}")

        return round(costo, 2)

    def describir_servicio(self) -> str:
        """Descripcion detallada del servicio de reserva de salas."""
        return (f"Sala '{self.nombre}' - Tipo: {self._tipo_sala} | "
                f"Capacidad: {self._capacidad} personas | "
                f"Precio/hora: ${self._precio_base:.2f}")

    def validar(self) -> bool:
        """Valida los datos de la sala."""
        return (self._capacidad > 0 and
                self._tipo_sala in self.TIPOS_SALA and
                self._precio_base > 0)


# ==================================================================
# SERVICIO 2: Alquiler de Equipos
# ==================================================================
class AlquilerEquipo(Servicio):
    """
    SERVICIO: Alquiler de Equipos

    Permite alquilar equipos tecnologicos. El costo varia
    segun:
      - Dias de alquiler
      - Tipo de equipo (laptop, proyector, servidor, etc.)
      - Seguro opcional
      - Impuestos
    """

    TIPOS_EQUIPO = {
        "laptop": 1.0,
        "proyector": 0.8,
        "servidor": 2.0,
        "impresora": 0.5,
        "videoconferencia": 1.5
    }

    def __init__(self, nombre: str, precio_base: float,
                 tipo_equipo: str, cantidad_disponible: int = 1):
        """
        Constructor de AlquilerEquipo.

        Args:
            nombre (str): Nombre/identificador del equipo.
            precio_base (float): Precio por dia.
            tipo_equipo (str): Tipo de equipo.
            cantidad_disponible (int): Unidades disponibles.
        """
        super().__init__(nombre, precio_base)

        tipo_equipo = tipo_equipo.lower()
        if tipo_equipo not in self.TIPOS_EQUIPO:
            raise ServicioError(
                f"Tipo de equipo '{tipo_equipo}' no valido. "
                f"Opciones: {list(self.TIPOS_EQUIPO.keys())}",
                "SER-020"
            )

        if cantidad_disponible < 0:
            raise ServicioError(
                f"La cantidad disponible no puede ser negativa",
                "SER-021"
            )

        self._tipo_equipo = tipo_equipo
        self._cantidad_disponible = cantidad_disponible

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    @property
    def cantidad_disponible(self) -> int:
        return self._cantidad_disponible

    def calcular_costo(self, dias: int, con_seguro: bool = False,
                       aplicar_impuesto: bool = False) -> float:
        """
        SOBRECARGA: calcular_costo

        Variantes de uso:
          - calcular_costo(dias)
          - calcular_costo(dias, con_seguro=True)
          - calcular_costo(dias, True, aplicar_impuesto=True)

        Formula:
          costo = precio_base x dias x factor_tipo
          Si hay seguro: costo x 1.10 (10% adicional)
          Si aplica impuesto: costo x 1.19
        """
        if dias <= 0:
            raise DatosInvalidosError(
                f"Los dias deben ser positivos, se recibio {dias}",
                "DAT-020"
            )

        factor_tipo = self.TIPOS_EQUIPO[self._tipo_equipo]
        costo = self._precio_base * dias * factor_tipo

        if con_seguro:
            costo *= 1.10  # 10% de seguro
            Logger.info(f"Seguro (10%) aplicado a equipo {self.nombre}")

        if aplicar_impuesto:
            costo *= 1.19
            Logger.info(f"Impuesto (19%) aplicado a equipo {self.nombre}")

        return round(costo, 2)

    def describir_servicio(self) -> str:
        """Descripcion del servicio de alquiler de equipos."""
        return (f"Equipo '{self.nombre}' - Tipo: {self._tipo_equipo} | "
                f"Disponibles: {self._cantidad_disponible} | "
                f"Precio/dia: ${self._precio_base:.2f}")

    def validar(self) -> bool:
        """Valida los datos del equipo."""
        return (self._cantidad_disponible >= 0 and
                self._tipo_equipo in self.TIPOS_EQUIPO)


# ==================================================================
# SERVICIO 3: Asesoria Especializada
# ==================================================================
class AsesoriaEspecializada(Servicio):
    """
    SERVICIO: Asesoria Especializada

    Permite contratar asesorias con expertos. El costo varia
    segun:
      - Horas de asesoria
      - Nivel del asesor (junior, senior, experto)
      - Modalidad (presencial, virtual)
      - Descuentos por paquetes
    """

    NIVELES_ASESOR = {
        "junior": 1.0,
        "senior": 1.8,
        "experto": 3.0
    }

    MODALIDADES = {
        "virtual": 1.0,
        "presencial": 1.3
    }

    def __init__(self, nombre: str, precio_base: float,
                 nivel_asesor: str = "senior", modalidad: str = "virtual"):
        """
        Constructor de AsesoriaEspecializada.

        Args:
            nombre (str): Nombre/titulo de la asesoria.
            precio_base (float): Precio por hora.
            nivel_asesor (str): Nivel del asesor.
            modalidad (str): Modalidad (virtual o presencial).
        """
        super().__init__(nombre, precio_base)

        nivel_asesor = nivel_asesor.lower()
        if nivel_asesor not in self.NIVELES_ASESOR:
            raise ServicioError(
                f"Nivel '{nivel_asesor}' no valido. "
                f"Opciones: {list(self.NIVELES_ASESOR.keys())}",
                "SER-030"
            )

        modalidad = modalidad.lower()
        if modalidad not in self.MODALIDADES:
            raise ServicioError(
                f"Modalidad '{modalidad}' no valida. "
                f"Opciones: {list(self.MODALIDADES.keys())}",
                "SER-031"
            )

        self._nivel_asesor = nivel_asesor
        self._modalidad = modalidad

    @property
    def nivel_asesor(self) -> str:
        return self._nivel_asesor

    @property
    def modalidad(self) -> str:
        return self._modalidad

    def calcular_costo(self, horas: float, descuento_paquete: float = 0.0,
                       aplicar_impuesto: bool = False) -> float:
        """
        SOBRECARGA: calcular_costo

        Variantes de uso:
          - calcular_costo(horas)
          - calcular_costo(horas, descuento_paquete=15.0)
          - calcular_costo(horas, 0.0, True)

        Formula:
          costo = precio_base x horas x factor_nivel x
                  factor_modalidad
          Si hay descuento paquete: costo x (1 - desc/100)
          Si aplica impuesto: costo x 1.19
        """
        if horas <= 0:
            raise DatosInvalidosError(
                f"Las horas deben ser positivas, se recibio {horas}",
                "DAT-030"
            )

        if descuento_paquete < 0 or descuento_paquete > 100:
            raise DatosInvalidosError(
                f"Descuento invalido: {descuento_paquete}",
                "DAT-031"
            )

        factor_nivel = self.NIVELES_ASESOR[self._nivel_asesor]
        factor_modalidad = self.MODALIDADES[self._modalidad]

        costo = self._precio_base * horas * factor_nivel * factor_modalidad

        if descuento_paquete > 0:
            costo *= (1 - descuento_paquete / 100)
            Logger.info(f"Descuento paquete {descuento_paquete}% "
                        f"aplicado a asesoria {self.nombre}")

        if aplicar_impuesto:
            costo *= 1.19
            Logger.info(f"Impuesto (19%) aplicado a asesoria {self.nombre}")

        return round(costo, 2)

    def describir_servicio(self) -> str:
        """Descripcion del servicio de asesoria."""
        return (f"Asesoria '{self.nombre}' - Nivel: {self._nivel_asesor} | "
                f"Modalidad: {self._modalidad} | "
                f"Precio/hora: ${self._precio_base:.2f}")

    def validar(self) -> bool:
        """Valida los datos de la asesoria."""
        return (self._nivel_asesor in self.NIVELES_ASESOR and
                self._modalidad in self.MODALIDADES) 

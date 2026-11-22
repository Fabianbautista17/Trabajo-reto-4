# ==================================================================
# ARCHIVO: reserva.py
# DESCRIPCION: Clase Reserva que integra cliente, servicio,
# duracion y estado. Implementa confirmacion, cancelacion y
# procesamiento con manejo robusto de excepciones.
# ==================================================================

from datetime import datetime
from entidad import Entidad
from cliente import Cliente
from servicio import Servicio
from excepciones import (ReservaError, OperacionNoPermitidaError,
                         DatosInvalidosError)
from logger import Logger


class Reserva(Entidad):
    """
    CLASE: Reserva

    Integra un cliente con un servicio especifico para un
    periodo determinado. Maneja estados:
      - PENDIENTE  -> Recien creada
      - CONFIRMADA -> Pagada y confirmada
      - CANCELADA  -> Cancelada por el cliente
      - COMPLETADA -> Servicio prestado

    PRINCIPIO: Composicion de objetos
      - Contiene referencias a Cliente y Servicio
    """

    ESTADOS = ["PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA"]

    def __init__(self, cliente: Cliente, servicio: Servicio,
                 duracion: float, fecha_reserva: datetime = None):
        """
        Constructor de Reserva.

        Args:
            cliente (Cliente): Cliente que realiza la reserva.
            servicio (Servicio): Servicio reservado.
            duracion (float): Duracion en horas o dias.
            fecha_reserva (datetime): Fecha de la reserva.
        """
        super().__init__()

        # Validacion de parametros
        if not isinstance(cliente, Cliente):
            raise ReservaError(
                "El cliente debe ser una instancia de la clase Cliente",
                "RES-001"
            )

        if not isinstance(servicio, Servicio):
            raise ReservaError(
                "El servicio debe ser una instancia de la clase Servicio",
                "RES-002"
            )

        if duracion <= 0:
            raise ReservaError(
                f"La duracion debe ser positiva, se recibio {duracion}",
                "RES-003"
            )

        if not cliente.activo:
            raise ReservaError(
                f"El cliente {cliente.nombre} no esta activo",
                "RES-004"
            )

        if not servicio.disponible:
            raise ReservaError(
                f"El servicio {servicio.nombre} no esta disponible",
                "RES-005"
            )

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._fecha_reserva = fecha_reserva or datetime.now()
        self._estado = "PENDIENTE"
        self._costo = 0.0

        Logger.info(f"Reserva creada: ID={self.id}, "
                    f"Cliente={cliente.nombre}, "
                    f"Servicio={servicio.nombre}")

    # ------------------------------------------------------------------
    # PROPIEDADES
    # ------------------------------------------------------------------

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion(self) -> float:
        return self._duracion

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo(self) -> float:
        return self._costo

    @property
    def fecha_reserva(self) -> datetime:
        return self._fecha_reserva

    # ------------------------------------------------------------------
    # METODOS DE GESTION DE RESERVA
    # ------------------------------------------------------------------

    def confirmar(self, metodo_pago: str = "efectivo") -> bool:
        """
        METODO: confirmar

        Confirma la reserva calculando el costo final.
        Solo se puede confirmar si esta en estado PENDIENTE.

        Usa try/except/else/finally para manejo robusto.
        """
        try:
            # Validar estado
            if self._estado != "PENDIENTE":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva en estado "
                    f"'{self._estado}'. Solo se pueden confirmar "
                    f"reservas PENDIENTES.",
                    "OPR-010"
                )

            # Validar metodo de pago
            metodos_validos = ["efectivo", "tarjeta", "transferencia", "nequi"]
            if metodo_pago.lower() not in metodos_validos:
                raise DatosInvalidosError(
                    f"Metodo de pago '{metodo_pago}' no valido. "
                    f"Opciones: {metodos_validos}",
                    "DAT-040"
                )

            # Calcular costo (polimorfismo - cada servicio calcula diferente)
            self._costo = self._servicio.calcular_costo(
                self._duracion, aplicar_impuesto=True
            )

            # Cambiar estado
            self._estado = "CONFIRMADA"

        except OperacionNoPermitidaError as e:
            Logger.error(f"Error al confirmar reserva {self.id}: {e}")
            raise
        except DatosInvalidosError as e:
            Logger.error(f"Datos invalidos al confirmar reserva {self.id}: {e}")
            raise
        except Exception as e:
            Logger.critical(f"Error inesperado al confirmar reserva {self.id}: {e}")
            raise ReservaError(f"Error inesperado: {e}", "RES-099")
        else:
            Logger.evento(f"Reserva {self.id} CONFIRMADA | "
                          f"Costo: ${self._costo:.2f} | "
                          f"Pago: {metodo_pago}")
        finally:
            Logger.info(f"Proceso de confirmacion finalizado para "
                        f"reserva {self.id}")

        return True

    def cancelar(self, motivo: str = "Sin motivo especificado") -> bool:
        """
        METODO: cancelar

        Cancela la reserva. Solo se puede cancelar si esta en
        estado PENDIENTE o CONFIRMADA.
        """
        try:
            if self._estado not in ["PENDIENTE", "CONFIRMADA"]:
                raise OperacionNoPermitidaError(
                    f"No se puede cancelar una reserva en estado "
                    f"'{self._estado}'",
                    "OPR-020"
                )

            self._estado = "CANCELADA"

        except OperacionNoPermitidaError as e:
            Logger.error(f"Error al cancelar reserva {self.id}: {e}")
            raise
        except Exception as e:
            Logger.critical(f"Error inesperado al cancelar reserva {self.id}: {e}")
            raise
        else:
            Logger.evento(f"Reserva {self.id} CANCELADA | "
                          f"Motivo: {motivo}")
        finally:
            Logger.info(f"Proceso de cancelacion finalizado para "
                        f"reserva {self.id}")

        return True

    def completar(self) -> bool:
        """
        Marca la reserva como completada (servicio prestado).
        """
        try:
            if self._estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"Solo se pueden completar reservas CONFIRMADAS. "
                    f"Estado actual: {self._estado}",
                    "OPR-030"
                )

            self._estado = "COMPLETADA"

        except OperacionNoPermitidaError as e:
            Logger.error(f"Error al completar reserva {self.id}: {e}")
            raise
        except Exception as e:
            Logger.critical(f"Error inesperado: {e}")
            raise
        else:
            Logger.evento(f"Reserva {self.id} COMPLETADA")
        finally:
            Logger.info(f"Servicio prestado para reserva {self.id}")

        return True

    # ------------------------------------------------------------------
    # METODOS IMPLEMENTADOS DE LA CLASE ABSTRACTA
    # ------------------------------------------------------------------

    def obtener_info(self) -> str:
        """Informacion completa de la reserva."""
        return (f"Reserva {self.id} | Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | "
                f"Duracion: {self._duracion} | "
                f"Costo: ${self._costo:.2f} | "
                f"Estado: {self._estado}")

    def validar(self) -> bool:
        """Valida la reserva."""
        return (isinstance(self._cliente, Cliente) and
                isinstance(self._servicio, Servicio) and
                self._duracion > 0 and
                self._estado in self.ESTADOS) 

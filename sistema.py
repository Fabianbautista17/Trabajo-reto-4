# ==================================================================
# ARCHIVO: sistema.py
# DESCRIPCION: Clase principal del sistema Software FJ.
# Gestiona clientes, servicios y reservas mediante listas
# internas (sin base de datos).
# ==================================================================

from cliente import Cliente
from servicio import Servicio
from reserva import Reserva
from excepciones import (SoftwareFJError, ClienteError, ServicioError,
                         ReservaError)
from logger import Logger


class SoftwareFJ:
    """
    CLASE: SoftwareFJ

    Sistema integral de gestion. Administra:
      - Lista de clientes
      - Catalogo de servicios
      - Registro de reservas

    Todas las operaciones tienen manejo de excepciones y
    registro en logs.
    """

    def __init__(self):
        """Constructor del sistema."""
        self._clientes = []
        self._servicios = []
        self._reservas = []
        Logger.evento("Sistema Software FJ inicializado")

    # ------------------------------------------------------------------
    # GESTION DE CLIENTES
    # ------------------------------------------------------------------

    def registrar_cliente(self, cedula: str, nombre: str,
                          email: str, telefono: str) -> Cliente:
        """
        Registra un nuevo cliente en el sistema.
        Valida que la cedula no este duplicada.
        """
        try:
            # Verificar duplicados
            for cliente in self._clientes:
                if cliente.cedula == cedula:
                    raise ClienteError(
                        f"Ya existe un cliente con cedula {cedula}",
                        "CLI-010"
                    )

            cliente = Cliente(cedula, nombre, email, telefono)
            self._clientes.append(cliente)
            Logger.evento(f"Cliente registrado: {nombre}")
            return cliente

        except ClienteError as e:
            Logger.error(f"Error al registrar cliente: {e}")
            raise
        except Exception as e:
            Logger.critical(f"Error inesperado al registrar cliente: {e}")
            raise

    def buscar_cliente(self, cedula: str) -> Cliente:
        """Busca un cliente por cedula."""
        for cliente in self._clientes:
            if cliente.cedula == cedula:
                return cliente
        raise ClienteError(
            f"No se encontro cliente con cedula {cedula}",
            "CLI-020"
        )

    def listar_clientes(self) -> list:
        """Retorna la lista de todos los clientes."""
        return self._clientes.copy()

    # ------------------------------------------------------------------
    # GESTION DE SERVICIOS
    # ------------------------------------------------------------------

    def agregar_servicio(self, servicio: Servicio):
        """Agrega un servicio al catalogo."""
        try:
            if not isinstance(servicio, Servicio):
                raise ServicioError(
                    "El objeto debe ser una instancia de Servicio",
                    "SER-050"
                )

            self._servicios.append(servicio)
            Logger.evento(f"Servicio agregado: {servicio.nombre}")

        except ServicioError as e:
            Logger.error(f"Error al agregar servicio: {e}")
            raise

    def buscar_servicio(self, nombre: str) -> Servicio:
        """Busca un servicio por nombre."""
        for servicio in self._servicios:
            if servicio.nombre.lower() == nombre.lower():
                return servicio
        raise ServicioError(
            f"No se encontro el servicio '{nombre}'",
            "SER-060"
        )

    def listar_servicios(self) -> list:
        """Retorna todos los servicios disponibles."""
        return [s for s in self._servicios if s.disponible]

    # ------------------------------------------------------------------
    # GESTION DE RESERVAS
    # ------------------------------------------------------------------

    def crear_reserva(self, cedula_cliente: str, nombre_servicio: str,
                      duracion: float) -> Reserva:
        """
        Crea una nueva reserva vinculando cliente y servicio.
        """
        try:
            cliente = self.buscar_cliente(cedula_cliente)
            servicio = self.buscar_servicio(nombre_servicio)

            reserva = Reserva(cliente, servicio, duracion)
            self._reservas.append(reserva)

            Logger.evento(f"Reserva creada: {reserva.id}")
            return reserva

        except (ClienteError, ServicioError, ReservaError) as e:
            Logger.error(f"Error al crear reserva: {e}")
            raise
        except Exception as e:
            Logger.critical(f"Error inesperado al crear reserva: {e}")
            raise

    def confirmar_reserva(self, id_reserva: str,
                          metodo_pago: str = "efectivo") -> bool:
        """Confirma una reserva existente."""
        reserva = self._buscar_reserva(id_reserva)
        return reserva.confirmar(metodo_pago)

    def cancelar_reserva(self, id_reserva: str,
                         motivo: str = "Sin motivo") -> bool:
        """Cancela una reserva existente."""
        reserva = self._buscar_reserva(id_reserva)
        return reserva.cancelar(motivo)

    def completar_reserva(self, id_reserva: str) -> bool:
        """Marca una reserva como completada."""
        reserva = self._buscar_reserva(id_reserva)
        return reserva.completar()

    def _buscar_reserva(self, id_reserva: str) -> Reserva:
        """Busca una reserva por ID."""
        for reserva in self._reservas:
            if reserva.id == id_reserva:
                return reserva
        raise ReservaError(
            f"No se encontro la reserva con ID {id_reserva}",
            "RES-070"
        )

    def listar_reservas(self) -> list:
        """Retorna todas las reservas."""
        return self._reservas.copy()

    # ------------------------------------------------------------------
    # REPORTES
    # ------------------------------------------------------------------

    def reporte_general(self) -> str:
        """Genera un reporte general del sistema."""
        reporte = []
        reporte.append("=" * 60)
        reporte.append("   REPORTE GENERAL - SOFTWARE FJ")
        reporte.append("=" * 60)
        reporte.append(f"Clientes registrados: {len(self._clientes)}")
        reporte.append(f"Servicios en catalogo: {len(self._servicios)}")
        reporte.append(f"Total de reservas: {len(self._reservas)}")

        estados = {}
        for r in self._reservas:
            estados[r.estado] = estados.get(r.estado, 0) + 1
        reporte.append(f"Por estado: {estados}")

        ingresos = sum(r.costo for r in self._reservas
                       if r.estado in ["CONFIRMADA", "COMPLETADA"])
        reporte.append(f"Ingresos totales: ${ingresos:.2f}")
        reporte.append("=" * 60)

        return "\n".join(reporte) 

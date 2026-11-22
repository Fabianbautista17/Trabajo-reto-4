# ==================================================================
# ARCHIVO: excepciones.py
# DESCRIPCION: Define todas las excepciones personalizadas del
# sistema. Cada excepcion representa un tipo especifico de error
# que puede ocurrir durante la operacion del sistema.
# EMPRESA: Software FJ
# FECHA: 22 de noviembre de 2026
# ==================================================================


class SoftwareFJError(Exception):
    """
    EXCEPCION BASE
    Clase padre de todas las excepciones del sistema.
    Permite capturar cualquier error del sistema con un solo
    bloque except SoftwareFJError.
    """
    def __init__(self, mensaje: str, codigo: str = "ERR-000"):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")


class ClienteError(SoftwareFJError):
    """
    EXCEPCION DE CLIENTE
    Se lanza cuando hay problemas con datos de clientes:
    - Cedula invalida
    - Nombre vacio o con caracteres no permitidos
    - Email con formato incorrecto
    - Telefono invalido
    """
    def __init__(self, mensaje: str, codigo: str = "CLI-001"):
        super().__init__(mensaje, codigo)


class ServicioError(SoftwareFJError):
    """
    EXCEPCION DE SERVICIO
    Se lanza cuando:
    - El servicio no existe
    - Parametros del servicio son invalidos
    - El servicio no esta disponible
    """
    def __init__(self, mensaje: str, codigo: str = "SER-001"):
        super().__init__(mensaje, codigo)


class ReservaError(SoftwareFJError):
    """
    EXCEPCION DE RESERVA
    Se lanza cuando:
    - Intento de reserva incorrecto
    - Conflicto de horarios
    - Cancelacion no permitida
    - Estado de reserva invalido
    """
    def __init__(self, mensaje: str, codigo: str = "RES-001"):
        super().__init__(mensaje, codigo)


class DatosInvalidosError(SoftwareFJError):
    """
    EXCEPCION DE DATOS INVALIDOS
    Se lanza cuando los datos de entrada no cumplen con el
    formato o las restricciones esperadas.
    """
    def __init__(self, mensaje: str, codigo: str = "DAT-001"):
        super().__init__(mensaje, codigo)


class OperacionNoPermitidaError(SoftwareFJError):
    """
    EXCEPCION DE OPERACION NO PERMITIDA
    Se lanza cuando se intenta realizar una accion que no esta
    permitida segun el estado actual del objeto.
    """
    def __init__(self, mensaje: str, codigo: str = "OPR-001"):
        super().__init__(mensaje, codigo) 

# ==================================================================
# ARCHIVO: logger.py
# DESCRIPCION: Sistema de registro de eventos y errores.
# Todos los errores y eventos relevantes del sistema se
# registran en el archivo 'software_fj.log' para mantener un
# historial completo de la operacion del sistema.
# ==================================================================

import os
from datetime import datetime


class Logger:
    """
    CLASE LOGGER
    Gestiona el registro de eventos, informacion, advertencias
    y errores en un archivo de log.

    Niveles de log:
      - INFO: Eventos normales del sistema
      - WARNING: Advertencias que no detienen la ejecucion
      - ERROR: Errores que afectan una operacion especifica
      - CRITICAL: Errores graves del sistema
    """

    # Nombre del archivo de log
    ARCHIVO_LOG = "software_fj.log"

    @classmethod
    def _escribir_log(cls, nivel: str, mensaje: str):
        """
        METODO PRIVADO: _escribir_log
        Escribe una entrada en el archivo de log con formato:
        [FECHA HORA] [NIVEL] mensaje
        """
        try:
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entrada = f"[{fecha_hora}] [{nivel}] {mensaje}\n"

            # Abrir archivo en modo append (agregar al final)
            with open(cls.ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
                archivo.write(entrada)

        except Exception as e:
            # Si falla el log, imprimir en consola como ultimo recurso
            print(f"Advertencia: Error al escribir en log: {e}")

    @classmethod
    def info(cls, mensaje: str):
        """Registra un evento informativo."""
        cls._escribir_log("INFO", mensaje)
        print(f"[INFO] {mensaje}")

    @classmethod
    def warning(cls, mensaje: str):
        """Registra una advertencia."""
        cls._escribir_log("WARNING", mensaje)
        print(f"[WARNING] {mensaje}")

    @classmethod
    def error(cls, mensaje: str):
        """Registra un error."""
        cls._escribir_log("ERROR", mensaje)
        print(f"[ERROR] {mensaje}")

    @classmethod
    def critical(cls, mensaje: str):
        """Registra un error critico."""
        cls._escribir_log("CRITICAL", mensaje)
        print(f"[CRITICAL] {mensaje}")

    @classmethod
    def evento(cls, mensaje: str):
        """Registra un evento especial del sistema."""
        cls._escribir_log("EVENTO", mensaje)
        print(f"[EVENTO] {mensaje}")

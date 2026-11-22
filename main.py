# ==================================================================
# ARCHIVO: main.py
# DESCRIPCION: Programa principal que demuestra el funcionamiento
# completo del sistema Software FJ. Ejecuta al menos 10
# operaciones completas incluyendo casos validos e invalidos.
#
# OPERACIONES DEMOSTRADAS:
#   1. Registro valido de cliente
#   2. Registro invalido de cliente (cedula erronea)
#   3. Registro invalido de cliente (email erroneo)
#   4. Creacion de servicios
#   5. Reserva exitosa
#   6. Reserva fallida (cliente no existe)
#   7. Confirmacion de reserva
#   8. Cancelacion de reserva
#   9. Completar reserva
#  10. Operacion no permitida (doble confirmacion)
#  11. Reporte general del sistema
# ==================================================================

from sistema import SoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import (SoftwareFJError, ClienteError, ServicioError,
                         ReservaError, DatosInvalidosError,
                         OperacionNoPermitidaError)
from logger import Logger


def separador(titulo: str):
    """Imprime un separador visual con titulo."""
    print(f"\n{'=' * 65}")
    print(f"  {titulo}")
    print(f"{'=' * 65}")


def main():
    """
    FUNCION PRINCIPAL

    Ejecuta 11 operaciones completas demostrando:
      - Casos validos (operaciones exitosas)
      - Casos invalidos (manejo de excepciones)
      - Polimorfismo en calculo de costos
      - Herencia y abstraccion
      - Encapsulacion de datos
      - Manejo robusto de excepciones
    """

    # Inicializar el sistema
    sistema = SoftwareFJ()

    # ==================================================================
    # OPERACION 1: Registro valido de cliente
    # ==================================================================
    separador("OPERACION 1: Registro valido de cliente")
    try:
        cliente1 = sistema.registrar_cliente(
            cedula="1001234567",
            nombre="Juan Perez",
            email="juan.perez@email.com",
            telefono="3001234567"
        )
        print(f"Cliente registrado: {cliente1.obtener_info()}")
    except SoftwareFJError as e:
        print(f"Error: {e}")

    # ==================================================================
    # OPERACION 2: Registro invalido (cedula con letras)
    # ==================================================================
    separador("OPERACION 2: Registro invalido - Cedula con letras")
    try:
        sistema.registrar_cliente(
            cedula="ABC1234567",  # Invalido
            nombre="Maria Lopez",
            email="maria@email.com",
            telefono="3009876543"
        )
    except ClienteError as e:
        print(f"Capturado correctamente: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    # ==================================================================
    # OPERACION 3: Registro invalido (email sin formato)
    # ==================================================================
    separador("OPERACION 3: Registro invalido - Email incorrecto")
    try:
        sistema.registrar_cliente(
            cedula="1009876543",
            nombre="Carlos Ruiz",
            email="email-invalido",  # Invalido
            telefono="3101234567"
        )
    except ClienteError as e:
        print(f"Capturado correctamente: {e}")

    # ==================================================================
    # OPERACION 4: Registro de segundo cliente valido
    # ==================================================================
    separador("OPERACION 4: Segundo cliente valido")
    try:
        cliente2 = sistema.registrar_cliente(
            cedula="1009876543",
            nombre="Carlos Ruiz",
            email="carlos.ruiz@email.com",
            telefono="3101234567"
        )
        print(f"Cliente registrado: {cliente2.obtener_info()}")
    except SoftwareFJError as e:
        print(f"Error: {e}")

    # ==================================================================
    # OPERACION 5: Creacion de servicios (3 tipos)
    # ==================================================================
    separador("OPERACION 5: Creacion de servicios")

    try:
        # Servicio 1: Reserva de Sala Ejecutiva
        sala_ejecutiva = ReservaSala(
            nombre="Sala Ejecutiva A",
            precio_base=50000,
            capacidad=10,
            tipo_sala="ejecutiva"
        )
        sistema.agregar_servicio(sala_ejecutiva)
        print(f"Servicio creado: {sala_ejecutiva.describir_servicio()}")

        # Servicio 2: Alquiler de Laptop
        laptop = AlquilerEquipo(
            nombre="Laptop Dell XPS 15",
            precio_base=80000,
            tipo_equipo="laptop",
            cantidad_disponible=5
        )
        sistema.agregar_servicio(laptop)
        print(f"Servicio creado: {laptop.describir_servicio()}")

        # Servicio 3: Asesoria Senior Virtual
        asesoria = AsesoriaEspecializada(
            nombre="Asesoria en Desarrollo Web",
            precio_base=120000,
            nivel_asesor="senior",
            modalidad="virtual"
        )
        sistema.agregar_servicio(asesoria)
        print(f"Servicio creado: {asesoria.describir_servicio()}")

    except ServicioError as e:
        print(f"Error al crear servicio: {e}")

    # ==================================================================
    # OPERACION 6: Reserva exitosa
    # ==================================================================
    separador("OPERACION 6: Reserva exitosa")
    try:
        reserva1 = sistema.crear_reserva(
            cedula_cliente="1001234567",
            nombre_servicio="Sala Ejecutiva A",
            duracion=4  # 4 horas
        )
        print(f"Reserva creada: {reserva1.obtener_info()}")
    except SoftwareFJError as e:
        print(f"Error: {e}")

    # ==================================================================
    # OPERACION 7: Reserva fallida (cliente no existe)
    # ==================================================================
    separador("OPERACION 7: Reserva fallida - Cliente no existe")
    try:
        sistema.crear_reserva(
            cedula_cliente="9999999999",  # No existe
            nombre_servicio="Laptop Dell XPS 15",
            duracion=3
        )
    except ClienteError as e:
        print(f"Capturado correctamente: {e}")

    # ==================================================================
    # OPERACION 8: Confirmacion de reserva
    # ==================================================================
    separador("OPERACION 8: Confirmacion de reserva")
    try:
        sistema.confirmar_reserva(reserva1.id, metodo_pago="tarjeta")
        print(f"Reserva confirmada: {reserva1.obtener_info()}")
    except SoftwareFJError as e:
        print(f"Error: {e}")

    # ==================================================================
    # OPERACION 9: Crear y cancelar reserva
    # ==================================================================
    separador("OPERACION 9: Crear y cancelar reserva")
    try:
        reserva2 = sistema.crear_reserva(
            cedula_cliente="1009876543",
            nombre_servicio="Asesoria en Desarrollo Web",
            duracion=2
        )
        print(f"Reserva creada: {reserva2.obtener_info()}")

        sistema.cancelar_reserva(reserva2.id, motivo="Cambio de planes")
        print(f"Reserva cancelada: {reserva2.obtener_info()}")
    except SoftwareFJError as e:
        print(f"Error: {e}")

    # ==================================================================
    # OPERACION 10: Completar reserva
    # ==================================================================
    separador("OPERACION 10: Completar reserva")
    try:
        sistema.completar_reserva(reserva1.id)
        print(f"Reserva completada: {reserva1.obtener_info()}")
    except SoftwareFJError as e:
        print(f"Error: {e}")

    # ==================================================================
    # OPERACION 11: Operacion no permitida (doble confirmacion)
    # ==================================================================
    separador("OPERACION 11: Operacion no permitida")
    try:
        # Intentar confirmar una reserva ya completada
        sistema.confirmar_reserva(reserva1.id)
    except OperacionNoPermitidaError as e:
        print(f"Capturado correctamente: {e}")
    except SoftwareFJError as e:
        print(f"Error: {e}")

    # ==================================================================
    # OPERACION 12: Cancelar reserva ya completada (no permitido)
    # ==================================================================
    separador("OPERACION 12: Cancelar reserva completada (no permitido)")
    try:
        sistema.cancelar_reserva(reserva1.id)
    except OperacionNoPermitidaError as e:
        print(f"Capturado correctamente: {e}")

    # ==================================================================
    # OPERACION 13: Demostracion de polimorfismo en costos
    # ==================================================================
    separador("OPERACION 13: Polimorfismo - Calculo de costos")

    print("\nComparacion de costos entre servicios:")
    print(f"  Sala Ejecutiva (4h con impuesto): "
          f"${sala_ejecutiva.calcular_costo(4, aplicar_impuesto=True):,.2f}")
    print(f"  Laptop (3 dias con seguro): "
          f"${laptop.calcular_costo(3, con_seguro=True):,.2f}")
    print(f"  Asesoria Senior (2h virtual con descuento 10%): "
          f"${asesoria.calcular_costo(2, descuento_paquete=10.0):,.2f}")

    # ==================================================================
    # OPERACION 14: Reporte general
    # ==================================================================
    separador("OPERACION 14: Reporte General del Sistema")
    print(sistema.reporte_general())

    # ==================================================================
    # OPERACION 15: Listar todos los clientes y reservas
    # ==================================================================
    separador("OPERACION 15: Listado completo")

    print("\nCLIENTES REGISTRADOS:")
    for cliente in sistema.listar_clientes():
        print(f"  - {cliente.obtener_info()}")

    print("\nSERVICIOS DISPONIBLES:")
    for servicio in sistema.listar_servicios():
        print(f"  - {servicio.obtener_info()}")

    print("\nTODAS LAS RESERVAS:")
    for reserva in sistema.listar_reservas():
        print(f"  - {reserva.obtener_info()}")

    # ==================================================================
    # FIN DEL PROGRAMA
    # ==================================================================
    separador("SISTEMA SOFTWARE FJ - EJECUCION COMPLETADA")
    print(f"\nRevisa el archivo 'software_fj.log' para ver el registro completo")
    print(f"de todos los eventos y errores del sistema.\n")


# ==================================================================
# EJECUCION
# ==================================================================
if __name__ == "__main__":
    main() 

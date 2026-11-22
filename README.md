# Software FJ - Sistema Integral de Gestion

## Descripcion

Sistema orientado a objetos para la gestion de clientes, servicios y reservas
de la empresa Software FJ, sin uso de bases de datos.

## Principios POO Implementados

- Abstraccion: Clases abstractas Entidad y Servicio
- Herencia: Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada heredan de clases base
- Polimorfismo: Metodo calcular_costo() implementado diferente en cada servicio
- Encapsulacion: Atributos privados con getters/setters validados
- Manejo de Excepciones: Excepciones personalizadas y bloques try/except/else/finally

## Estructura del Proyecto

SoftwareFJ/
├── README.md              Este archivo
├── excepciones.py         Excepciones personalizadas
├── logger.py              Sistema de logs
├── entidad.py             Clase abstracta base
├── cliente.py             Clase Cliente
├── servicio.py            Clase abstracta Servicio
├── servicios.py           3 servicios especializados
├── reserva.py             Clase Reserva
├── sistema.py             Sistema principal
└── main.py                Programa principal

## Requisitos

- Python 3.10 o superior
- No requiere librerias externas

## Ejecucion

python main.py

## Funcionalidades del Sistema

1. Registro de clientes con validaciones robustas
2. Gestion de tres tipos de servicios:
   - Reserva de Salas (basica, ejecutiva, auditorio)
   - Alquiler de Equipos (laptop, proyector, servidor, etc.)
   - Asesorias Especializadas (junior, senior, experto)
3. Creacion, confirmacion, cancelacion y completado de reservas
4. Calculo de costos con impuestos, descuentos y seguros
5. Sistema de logs para registro de eventos y errores
6. Manejo de excepciones personalizadas

## Operaciones Demostradas en main.py

1. Registro valido de cliente
2. Registro invalido de cliente (cedula con letras)
3. Registro invalido de cliente (email sin formato)
4. Registro de segundo cliente valido
5. Creacion de tres servicios especializados
6. Reserva exitosa
7. Reserva fallida (cliente no existe)
8. Confirmacion de reserva
9. Crear y cancelar reserva
10. Completar reserva
11. Operacion no permitida (doble confirmacion)
12. Cancelar reserva ya completada (no permitido)
13. Demostracion de polimorfismo en calculo de costos
14. Reporte general del sistema
15. Listado completo de clientes, servicios y reservas

## Autor

FBAUTISTA - Universidad Nacional Abierta y a Distancia (UNAD)
Fecha: 22 de noviembre de 2026

## Licencia

Proyecto academico desarrollado para la Universidad Nacional Abierta y a Distancia (UNAD). 

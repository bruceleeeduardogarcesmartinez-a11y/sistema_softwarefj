# =============================================================
# SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ
# Universidad Nacional Abierta y a Distancia (UNAD)
# Curso: Programación - Código: 213023
# =============================================================

from clases.cliente import Cliente  # importa elementos necesarios desde otro modulo
from clases.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada  # importa elementos necesarios desde otro modulo
from clases.reserva import Reserva  # importa elementos necesarios desde otro modulo
from clases.excepciones import ClienteInvalidoError, ServicioNoDisponibleError, ReservaInvalidaError  # importa elementos necesarios desde otro modulo
from utils.logger import Logger  # importa elementos necesarios desde otro modulo

logger = Logger("logs/sistema.log")  # asigna o actualiza el valor de logger

def separador(titulo):  # define la funcion o metodo separador
    print(f"\n{'='*55}")  # asigna o actualiza el valor de print f n
    print(f"  {titulo}")  # ejecuta esta instruccion del programa
    print(f"{'='*55}")  # asigna o actualiza el valor de print f

def main():  # define la funcion o metodo main
    print("\n" + "="*55)  # asigna o actualiza el valor de print n
    print("   SISTEMA DE GESTIÓN - SOFTWARE FJ")  # ejecuta esta instruccion del programa
    print("="*55)  # asigna o actualiza el valor de print

    # -------------------------------------------------------
    # OPERACIÓN 1: Registrar cliente válido
    # -------------------------------------------------------
    separador("OP 1 - Registrar cliente válido")  # ejecuta esta instruccion del programa
    try:  # inicia un bloque que puede generar excepciones
        c1 = Cliente("001", "Ana Torres", "ana@email.com", "3001234567")  # asigna o actualiza el valor de c1
        print(f"✅ Cliente registrado: {c1}")  # ejecuta esta instruccion del programa
        logger.registrar_evento(f"Cliente registrado: {c1.get_nombre()}")  # ejecuta esta instruccion del programa
    except ClienteInvalidoError as e:  # captura y maneja una excepcion
        print(f"❌ Error: {e}")  # ejecuta esta instruccion del programa
        logger.registrar_error(str(e))  # ejecuta esta instruccion del programa

    # -------------------------------------------------------
    # OPERACIÓN 2: Registrar cliente con nombre vacío (inválido)
    # -------------------------------------------------------
    separador("OP 2 - Cliente con nombre vacío (error esperado)")  # ejecuta esta instruccion del programa
    try:  # inicia un bloque que puede generar excepciones
        c2 = Cliente("002", "", "sin@nombre.com", "3009999999")  # asigna o actualiza el valor de c2
        print(f"✅ Cliente registrado: {c2}")  # ejecuta esta instruccion del programa
    except ClienteInvalidoError as e:  # captura y maneja una excepcion
        print(f"❌ Error capturado: {e}")  # ejecuta esta instruccion del programa
        logger.registrar_error(f"Cliente inválido: {e}")  # ejecuta esta instruccion del programa
    finally:  # ejecuta acciones finales del bloque
        print("   [finally] Validación de cliente completada.")  # ejecuta esta instruccion del programa

    # -------------------------------------------------------
    # OPERACIÓN 3: Registrar cliente con correo inválido
    # -------------------------------------------------------
    separador("OP 3 - Cliente con correo inválido (error esperado)")  # ejecuta esta instruccion del programa
    try:  # inicia un bloque que puede generar excepciones
        c3 = Cliente("003", "Luis Pérez", "correo-sin-arroba", "3112345678")  # asigna o actualiza el valor de c3
        print(f"✅ Cliente: {c3}")  # ejecuta esta instruccion del programa
    except ClienteInvalidoError as e:  # captura y maneja una excepcion
        print(f"❌ Error capturado: {e}")  # ejecuta esta instruccion del programa
        logger.registrar_error(f"Correo inválido: {e}")  # ejecuta esta instruccion del programa
    else:  # ejecuta el bloque cuando no se cumple la condicion anterior
        print("   [else] No hubo errores.")  # ejecuta esta instruccion del programa
    finally:  # ejecuta acciones finales del bloque
        print("   [finally] Proceso terminado.")  # ejecuta esta instruccion del programa

    # -------------------------------------------------------
    # OPERACIÓN 4: Crear servicios válidos
    # -------------------------------------------------------
    separador("OP 4 - Crear servicios")  # ejecuta esta instruccion del programa
    try:  # inicia un bloque que puede generar excepciones
        sala = ReservaSala("S01", "Sala Conferencias A", capacidad=20)  # asigna o actualiza el valor de sala
        equipo = AlquilerEquipo("E01", "Laptop HP ProBook", tipo_equipo="laptop")  # asigna o actualiza el valor de equipo
        asesoria = AsesoriaEspecializada("A01", "Asesoría Python Avanzado", especialidad="Python")  # asigna o actualiza el valor de asesoria
        print(f"✅ {sala}")  # ejecuta esta instruccion del programa
        print(f"✅ {equipo}")  # ejecuta esta instruccion del programa
        print(f"✅ {asesoria}")  # ejecuta esta instruccion del programa
        logger.registrar_evento("Tres servicios creados correctamente.")  # ejecuta esta instruccion del programa
    except Exception as e:  # captura y maneja una excepcion
        print(f"❌ Error: {e}")  # ejecuta esta instruccion del programa
        logger.registrar_error(str(e))  # ejecuta esta instruccion del programa

    # -------------------------------------------------------
    # OPERACIÓN 5: Crear servicio inválido (capacidad negativa)
    # -------------------------------------------------------
    separador("OP 5 - Servicio con capacidad inválida (error esperado)")  # ejecuta esta instruccion del programa
    try:  # inicia un bloque que puede generar excepciones
        sala_mala = ReservaSala("S99", "Sala Inválida", capacidad=-5)  # asigna o actualiza el valor de sala mala
        print(f"✅ {sala_mala}")  # ejecuta esta instruccion del programa
    except ServicioNoDisponibleError as e:  # captura y maneja una excepcion
        print(f"❌ Error capturado: {e}")  # ejecuta esta instruccion del programa
        logger.registrar_error(f"Servicio inválido: {e}")  # ejecuta esta instruccion del programa

    # -------------------------------------------------------
    # OPERACIÓN 6: Calcular costos con polimorfismo
    # -------------------------------------------------------
    separador("OP 6 - Calcular costos (polimorfismo)")  # ejecuta esta instruccion del programa
    try:  # inicia un bloque que puede generar excepciones
        servicios = [sala, equipo, asesoria]  # asigna o actualiza el valor de servicios
        for s in servicios:  # recorre una coleccion elemento por elemento
            costo_base = s.calcular_costo(horas=3)  # asigna o actualiza el valor de costo base
            costo_iva = s.calcular_costo(horas=3, con_iva=True)  # asigna o actualiza el valor de costo iva
            costo_desc = s.calcular_costo(horas=3, descuento=0.10)  # asigna o actualiza el valor de costo desc
            print(f"   {s.get_nombre()}: base=${costo_base:,.0f} | +IVA=${costo_iva:,.0f} | -10%=${costo_desc:,.0f}")  # asigna o actualiza el valor de print f s get nombre base
        logger.registrar_evento("Cálculo de costos exitoso.")  # ejecuta esta instruccion del programa
    except Exception as e:  # captura y maneja una excepcion
        print(f"❌ Error: {e}")  # ejecuta esta instruccion del programa
        logger.registrar_error(str(e))  # ejecuta esta instruccion del programa

    # -------------------------------------------------------
    # OPERACIÓN 7: Crear reserva válida
    # -------------------------------------------------------
    separador("OP 7 - Crear reserva válida")  # ejecuta esta instruccion del programa
    try:  # inicia un bloque que puede generar excepciones
        r1 = Reserva("R001", c1, sala, duracion_horas=4)  # asigna o actualiza el valor de r1
        r1.confirmar()  # ejecuta esta instruccion del programa
        print(f"✅ {r1}")  # ejecuta esta instruccion del programa
        logger.registrar_evento(f"Reserva confirmada: {r1.get_id()}")  # ejecuta esta instruccion del programa
    except ReservaInvalidaError as e:  # captura y maneja una excepcion
        print(f"❌ Error: {e}")  # ejecuta esta instruccion del programa
        logger.registrar_error(str(e))  # ejecuta esta instruccion del programa

    # -------------------------------------------------------
    # OPERACIÓN 8: Crear reserva con duración inválida
    # -------------------------------------------------------
    separador("OP 8 - Reserva con duración 0 (error esperado)")  # ejecuta esta instruccion del programa
    try:  # inicia un bloque que puede generar excepciones
        r2 = Reserva("R002", c1, equipo, duracion_horas=0)  # asigna o actualiza el valor de r2
        r2.confirmar()  # ejecuta esta instruccion del programa
        print(f"✅ {r2}")  # ejecuta esta instruccion del programa
    except ReservaInvalidaError as e:  # captura y maneja una excepcion
        print(f"❌ Error capturado: {e}")  # ejecuta esta instruccion del programa
        logger.registrar_error(f"Reserva inválida: {e}")  # ejecuta esta instruccion del programa
    finally:  # ejecuta acciones finales del bloque
        print("   [finally] Intento de reserva procesado.")  # ejecuta esta instruccion del programa

    # -------------------------------------------------------
    # OPERACIÓN 9: Cancelar una reserva
    # -------------------------------------------------------
    separador("OP 9 - Cancelar reserva")  # ejecuta esta instruccion del programa
    try:  # inicia un bloque que puede generar excepciones
        r3 = Reserva("R003", c1, asesoria, duracion_horas=2)  # asigna o actualiza el valor de r3
        r3.confirmar()  # ejecuta esta instruccion del programa
        print(f"   Antes: {r3}")  # ejecuta esta instruccion del programa
        r3.cancelar()  # ejecuta esta instruccion del programa
        print(f"   Después: {r3}")  # ejecuta esta instruccion del programa
        logger.registrar_evento(f"Reserva cancelada: {r3.get_id()}")  # ejecuta esta instruccion del programa
    except ReservaInvalidaError as e:  # captura y maneja una excepcion
        print(f"❌ Error: {e}")  # ejecuta esta instruccion del programa
        logger.registrar_error(str(e))  # ejecuta esta instruccion del programa

    # -------------------------------------------------------
    # OPERACIÓN 10: Encadenamiento de excepciones
    # -------------------------------------------------------
    separador("OP 10 - Encadenamiento de excepciones")  # ejecuta esta instruccion del programa
    try:  # inicia un bloque que puede generar excepciones
        try:  # inicia un bloque que puede generar excepciones
            c_enc = Cliente("004", "Carlos Ruiz", "carlos@email.com", "abc")  # teléfono inválido
        except ClienteInvalidoError as e:  # captura y maneja una excepcion
            raise ReservaInvalidaError("No se pudo crear reserva porque el cliente es inválido") from e  # lanza una excepcion con un mensaje
    except ReservaInvalidaError as e:  # captura y maneja una excepcion
        print(f"❌ Error encadenado: {e}")  # ejecuta esta instruccion del programa
        if e.__cause__:  # evalua una condicion para decidir el flujo
            print(f"   Causa original: {e.__cause__}")  # ejecuta esta instruccion del programa
        logger.registrar_error(f"Excepción encadenada: {e} | Causa: {e.__cause__}")  # ejecuta esta instruccion del programa
    finally:  # ejecuta acciones finales del bloque
        print("   [finally] Flujo de encadenamiento finalizado.")  # ejecuta esta instruccion del programa

    # -------------------------------------------------------
    # RESUMEN FINAL
    # -------------------------------------------------------
    separador("RESUMEN DEL SISTEMA")  # ejecuta esta instruccion del programa
    print("  10 operaciones ejecutadas.")  # ejecuta esta instruccion del programa
    print("  Errores manejados sin interrumpir el sistema.")  # ejecuta esta instruccion del programa
    print("  Log guardado en: logs/sistema.log")  # ejecuta esta instruccion del programa
    print(f"{'='*55}\n")  # asigna o actualiza el valor de print f
    logger.registrar_evento("Sistema finalizado correctamente.")  # ejecuta esta instruccion del programa

if __name__ == "__main__":  # evalua una condicion para decidir el flujo
    main()  # ejecuta esta instruccion del programa

# =============================================================
# LOGGER - SOFTWARE FJ
# Registro de eventos y errores en archivo de logs
# =============================================================

import os  # importa un modulo requerido por el programa
from datetime import datetime  # importa elementos necesarios desde otro modulo
from clases.excepciones import LogError  # importa elementos necesarios desde otro modulo


class Logger:  # define la clase Logger
    """
    Clase utilitaria para registrar eventos y errores en un archivo de log.
    Mantiene el historial de operaciones del sistema.
    """

    def __init__(self, ruta_archivo: str):  # define la funcion o metodo __init__
        self.__ruta = ruta_archivo  # asigna o actualiza el valor de ruta
        self.__inicializar_archivo()  # ejecuta esta instruccion del programa

    def __inicializar_archivo(self):  # define la funcion o metodo __inicializar_archivo
        """Crea el directorio y archivo de log si no existen."""
        try:  # inicia un bloque que puede generar excepciones
            directorio = os.path.dirname(self.__ruta)  # asigna o actualiza el valor de directorio
            if directorio and not os.path.exists(directorio):  # evalua una condicion para decidir el flujo
                os.makedirs(directorio)  # ejecuta esta instruccion del programa
            # Encabezado inicial
            if not os.path.exists(self.__ruta):  # evalua una condicion para decidir el flujo
                with open(self.__ruta, "w", encoding="utf-8") as f:  # abre y administra un recurso temporal
                    f.write("=" * 60 + "\n")  # escribe informacion en el archivo
                    f.write("  LOG DEL SISTEMA - SOFTWARE FJ\n")  # escribe informacion en el archivo
                    f.write(f"  Iniciado: {self.__timestamp()}\n")  # escribe informacion en el archivo
                    f.write("=" * 60 + "\n\n")  # escribe informacion en el archivo
        except OSError as e:  # captura y maneja una excepcion
            raise LogError(f"No se pudo inicializar el archivo de log: {e}")  # lanza una excepcion con un mensaje

    def __timestamp(self) -> str:  # define la funcion o metodo __timestamp
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # devuelve un valor al llamador

    def __escribir(self, nivel: str, mensaje: str):  # define la funcion o metodo __escribir
        try:  # inicia un bloque que puede generar excepciones
            with open(self.__ruta, "a", encoding="utf-8") as f:  # abre y administra un recurso temporal
                f.write(f"[{self.__timestamp()}] [{nivel}] {mensaje}\n")  # escribe informacion en el archivo
        except OSError as e:  # captura y maneja una excepcion
            raise LogError(f"Error al escribir en el log: {e}")  # lanza una excepcion con un mensaje

    def registrar_evento(self, mensaje: str):  # define la funcion o metodo registrar_evento
        """Registra un evento informativo."""
        self.__escribir("INFO", mensaje)  # ejecuta esta instruccion del programa

    def registrar_error(self, mensaje: str):  # define la funcion o metodo registrar_error
        """Registra un error."""
        self.__escribir("ERROR", mensaje)  # ejecuta esta instruccion del programa

    def registrar_advertencia(self, mensaje: str):  # define la funcion o metodo registrar_advertencia
        """Registra una advertencia."""
        self.__escribir("ADVERTENCIA", mensaje)  # ejecuta esta instruccion del programa

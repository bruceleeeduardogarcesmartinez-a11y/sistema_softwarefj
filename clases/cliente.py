# =============================================================
# CLASE CLIENTE - SOFTWARE FJ
# Gestión de clientes con encapsulación y validaciones robustas
# =============================================================

import re  # importa un modulo requerido por el programa
from clases.entidad import Entidad  # importa elementos necesarios desde otro modulo
from clases.excepciones import ClienteInvalidoError  # importa elementos necesarios desde otro modulo


class Cliente(Entidad):  # define la clase Cliente
    """
    Clase que representa un cliente del sistema.
    Hereda de Entidad e implementa encapsulación y validaciones.
    """

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):  # define la funcion o metodo __init__
        try:  # inicia un bloque que puede generar excepciones
            super().__init__(id_cliente)  # inicializa la clase padre
        except ValueError as e:  # captura y maneja una excepcion
            raise ClienteInvalidoError(f"ID inválido: {e}")  # lanza una excepcion con un mensaje

        # Atributos privados (encapsulación)
        self.__nombre = None  # asigna o actualiza el valor de nombre
        self.__correo = None  # asigna o actualiza el valor de correo
        self.__telefono = None  # asigna o actualiza el valor de telefono

        # Se usan los setters para validar
        self.set_nombre(nombre)  # ejecuta esta instruccion del programa
        self.set_correo(correo)  # ejecuta esta instruccion del programa
        self.set_telefono(telefono)  # ejecuta esta instruccion del programa

    # ---- Setters con validación ----

    def set_nombre(self, nombre: str):  # define la funcion o metodo set_nombre
        if not nombre or not nombre.strip():  # evalua una condicion para decidir el flujo
            raise ClienteInvalidoError("El nombre del cliente no puede estar vacío.")  # lanza una excepcion con un mensaje
        if len(nombre.strip()) < 3:  # evalua una condicion para decidir el flujo
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")  # lanza una excepcion con un mensaje
        self.__nombre = nombre.strip()  # asigna o actualiza el valor de nombre

    def set_correo(self, correo: str):  # define la funcion o metodo set_correo
        patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'  # asigna o actualiza el valor de patron
        if not correo or not re.match(patron, correo):  # evalua una condicion para decidir el flujo
            raise ClienteInvalidoError(f"Correo electrónico inválido: '{correo}'")  # lanza una excepcion con un mensaje
        self.__correo = correo.strip()  # asigna o actualiza el valor de correo

    def set_telefono(self, telefono: str):  # define la funcion o metodo set_telefono
        if not telefono or not telefono.strip().isdigit():  # evalua una condicion para decidir el flujo
            raise ClienteInvalidoError(f"Teléfono inválido: '{telefono}'. Solo se permiten dígitos.")  # lanza una excepcion con un mensaje
        if len(telefono.strip()) < 7:  # evalua una condicion para decidir el flujo
            raise ClienteInvalidoError("El teléfono debe tener al menos 7 dígitos.")  # lanza una excepcion con un mensaje
        self.__telefono = telefono.strip()  # asigna o actualiza el valor de telefono

    # ---- Getters ----

    def get_nombre(self) -> str:  # define la funcion o metodo get_nombre
        return self.__nombre  # devuelve un valor al llamador

    def get_correo(self) -> str:  # define la funcion o metodo get_correo
        return self.__correo  # devuelve un valor al llamador

    def get_telefono(self) -> str:  # define la funcion o metodo get_telefono
        return self.__telefono  # devuelve un valor al llamador

    # ---- Métodos abstractos implementados ----

    def describir(self) -> str:  # define la funcion o metodo describir
        return (f"Cliente[{self.get_id()}] | Nombre: {self.__nombre} | "  # devuelve un valor al llamador
                f"Correo: {self.__correo} | Tel: {self.__telefono}")  # ejecuta esta instruccion del programa

    def validar(self) -> bool:  # define la funcion o metodo validar
        return bool(self.__nombre and self.__correo and self.__telefono)  # devuelve un valor al llamador

    def __str__(self):  # define la funcion o metodo __str__
        return self.describir()  # devuelve un valor al llamador

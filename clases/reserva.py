# =============================================================
# CLASE RESERVA - SOFTWARE FJ
# Integra Cliente + Servicio con estados y manejo de excepciones
# =============================================================

from clases.entidad import Entidad  # importa elementos necesarios desde otro modulo
from clases.cliente import Cliente  # importa elementos necesarios desde otro modulo
from clases.servicios import Servicio  # importa elementos necesarios desde otro modulo
from clases.excepciones import ReservaInvalidaError, ServicioNoDisponibleError  # importa elementos necesarios desde otro modulo


class Reserva(Entidad):  # define la clase Reserva
    """
    Representa una reserva que asocia un Cliente con un Servicio.
    Estados posibles: PENDIENTE → CONFIRMADA → CANCELADA
    """

    ESTADOS = ["PENDIENTE", "CONFIRMADA", "CANCELADA"]  # asigna o actualiza el valor de ESTADOS

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):  # define la funcion o metodo __init__
        try:  # inicia un bloque que puede generar excepciones
            super().__init__(id_reserva)  # inicializa la clase padre
        except ValueError as e:  # captura y maneja una excepcion
            raise ReservaInvalidaError(f"ID de reserva inválido: {e}")  # lanza una excepcion con un mensaje

        self.__validar_parametros(cliente, servicio, duracion_horas)  # ejecuta esta instruccion del programa

        self.__cliente = cliente  # asigna o actualiza el valor de cliente
        self.__servicio = servicio  # asigna o actualiza el valor de servicio
        self.__duracion_horas = duracion_horas  # asigna o actualiza el valor de duracion horas
        self.__estado = "PENDIENTE"  # asigna o actualiza el valor de estado
        self.__costo_total = 0.0  # asigna o actualiza el valor de costo total

    def __validar_parametros(self, cliente, servicio, duracion_horas):  # define la funcion o metodo __validar_parametros
        if not isinstance(cliente, Cliente):  # evalua una condicion para decidir el flujo
            raise ReservaInvalidaError("El parámetro 'cliente' debe ser una instancia de Cliente.")  # lanza una excepcion con un mensaje
        if not isinstance(servicio, Servicio):  # evalua una condicion para decidir el flujo
            raise ReservaInvalidaError("El parámetro 'servicio' debe ser una instancia de Servicio.")  # lanza una excepcion con un mensaje
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:  # evalua una condicion para decidir el flujo
            raise ReservaInvalidaError(  # lanza una excepcion con un mensaje
                f"La duración debe ser un número entero mayor a 0. Recibido: {duracion_horas}"  # ejecuta esta instruccion del programa
            )  # cierra la llamada o estructura anterior
        if not cliente.validar():  # evalua una condicion para decidir el flujo
            raise ReservaInvalidaError("El cliente asociado no es válido.")  # lanza una excepcion con un mensaje
        if not servicio.validar():  # evalua una condicion para decidir el flujo
            raise ReservaInvalidaError("El servicio asociado no está disponible.")  # lanza una excepcion con un mensaje

    def confirmar(self):  # define la funcion o metodo confirmar
        """Confirma la reserva y calcula el costo total."""
        try:  # inicia un bloque que puede generar excepciones
            if self.__estado == "CANCELADA":  # evalua una condicion para decidir el flujo
                raise ReservaInvalidaError("No se puede confirmar una reserva cancelada.")  # lanza una excepcion con un mensaje
            if self.__estado == "CONFIRMADA":  # evalua una condicion para decidir el flujo
                raise ReservaInvalidaError("La reserva ya está confirmada.")  # lanza una excepcion con un mensaje

            self.__costo_total = self.__servicio.calcular_costo(self.__duracion_horas)  # asigna o actualiza el valor de costo total
            self.__estado = "CONFIRMADA"  # asigna o actualiza el valor de estado

        except ServicioNoDisponibleError as e:  # captura y maneja una excepcion
            raise ReservaInvalidaError(  # lanza una excepcion con un mensaje
                f"No se pudo calcular el costo del servicio."  # ejecuta esta instruccion del programa
            ) from e  # ejecuta esta instruccion del programa

    def cancelar(self):  # define la funcion o metodo cancelar
        """Cancela la reserva."""
        try:  # inicia un bloque que puede generar excepciones
            if self.__estado == "CANCELADA":  # evalua una condicion para decidir el flujo
                raise ReservaInvalidaError("La reserva ya está cancelada.")  # lanza una excepcion con un mensaje
            self.__estado = "CANCELADA"  # asigna o actualiza el valor de estado
            self.__costo_total = 0.0  # asigna o actualiza el valor de costo total
        except ReservaInvalidaError:  # captura y maneja una excepcion
            raise  # ejecuta esta instruccion del programa

    def get_estado(self) -> str:  # define la funcion o metodo get_estado
        return self.__estado  # devuelve un valor al llamador

    def get_costo_total(self) -> float:  # define la funcion o metodo get_costo_total
        return self.__costo_total  # devuelve un valor al llamador

    def get_cliente(self) -> Cliente:  # define la funcion o metodo get_cliente
        return self.__cliente  # devuelve un valor al llamador

    def get_servicio(self) -> Servicio:  # define la funcion o metodo get_servicio
        return self.__servicio  # devuelve un valor al llamador

    def describir(self) -> str:  # define la funcion o metodo describir
        return (  # devuelve un valor al llamador
            f"Reserva[{self.get_id()}] | "  # ejecuta esta instruccion del programa
            f"Cliente: {self.__cliente.get_nombre()} | "  # ejecuta esta instruccion del programa
            f"Servicio: {self.__servicio.get_nombre()} | "  # ejecuta esta instruccion del programa
            f"Duración: {self.__duracion_horas}h | "  # ejecuta esta instruccion del programa
            f"Estado: {self.__estado} | "  # ejecuta esta instruccion del programa
            f"Costo: ${self.__costo_total:,.0f} COP"  # ejecuta esta instruccion del programa
        )  # cierra la llamada o estructura anterior

    def validar(self) -> bool:  # define la funcion o metodo validar
        return (  # devuelve un valor al llamador
            self.__estado in self.ESTADOS  # ejecuta esta instruccion del programa
            and self.__cliente.validar()  # ejecuta esta instruccion del programa
            and self.__servicio.validar()  # ejecuta esta instruccion del programa
        )  # cierra la llamada o estructura anterior

    def __str__(self):  # define la funcion o metodo __str__
        return self.describir()  # devuelve un valor al llamador

# =============================================================
# CLASES DE SERVICIOS - SOFTWARE FJ
# Clase abstracta Servicio + 3 servicios especializados
# Implementa polimorfismo y métodos sobrescritos
# =============================================================

from abc import abstractmethod  # importa elementos necesarios desde otro modulo
from clases.entidad import Entidad  # importa elementos necesarios desde otro modulo
from clases.excepciones import ServicioNoDisponibleError  # importa elementos necesarios desde otro modulo

IVA = 0.19  # 19% IVA Colombia


class Servicio(Entidad):  # define la clase Servicio
    """
    Clase abstracta que representa un servicio de Software FJ.
    Todas las clases de servicio heredan de esta.
    """

    def __init__(self, id_servicio: str, nombre: str, precio_hora: float):  # define la funcion o metodo __init__
        try:  # inicia un bloque que puede generar excepciones
            super().__init__(id_servicio)  # inicializa la clase padre
        except ValueError as e:  # captura y maneja una excepcion
            raise ServicioNoDisponibleError(f"ID de servicio inválido: {e}")  # lanza una excepcion con un mensaje

        if not nombre or not nombre.strip():  # evalua una condicion para decidir el flujo
            raise ServicioNoDisponibleError("El nombre del servicio no puede estar vacío.")  # lanza una excepcion con un mensaje
        if precio_hora <= 0:  # evalua una condicion para decidir el flujo
            raise ServicioNoDisponibleError(f"El precio por hora debe ser mayor a 0. Recibido: {precio_hora}")  # lanza una excepcion con un mensaje

        self.__nombre = nombre.strip()  # asigna o actualiza el valor de nombre
        self.__precio_hora = precio_hora  # asigna o actualiza el valor de precio hora
        self.__disponible = True  # asigna o actualiza el valor de disponible

    def get_nombre(self) -> str:  # define la funcion o metodo get_nombre
        return self.__nombre  # devuelve un valor al llamador

    def get_precio_hora(self) -> float:  # define la funcion o metodo get_precio_hora
        return self.__precio_hora  # devuelve un valor al llamador

    def esta_disponible(self) -> bool:  # define la funcion o metodo esta_disponible
        return self.__disponible  # devuelve un valor al llamador

    def set_disponible(self, estado: bool):  # define la funcion o metodo set_disponible
        self.__disponible = estado  # asigna o actualiza el valor de disponible

    # ---- Método sobrecargado con parámetros opcionales ----
    def calcular_costo(self, horas: int, con_iva: bool = False, descuento: float = 0.0) -> float:  # define la funcion o metodo calcular_costo
        """
        Calcula el costo del servicio.
        - horas: cantidad de horas contratadas
        - con_iva: si True, agrega IVA del 19%
        - descuento: porcentaje de descuento (0.0 a 1.0)
        """
        if horas <= 0:  # evalua una condicion para decidir el flujo
            raise ServicioNoDisponibleError("Las horas deben ser mayores a 0.")  # lanza una excepcion con un mensaje
        if not (0.0 <= descuento < 1.0):  # evalua una condicion para decidir el flujo
            raise ServicioNoDisponibleError("El descuento debe estar entre 0.0 y 0.99.")  # lanza una excepcion con un mensaje

        costo = self.__precio_hora * horas  # asigna o actualiza el valor de costo
        costo -= costo * descuento          # Aplica descuento
        if con_iva:  # evalua una condicion para decidir el flujo
            costo += costo * IVA            # Aplica IVA
        return round(costo, 2)  # devuelve un valor al llamador

    def validar(self) -> bool:  # define la funcion o metodo validar
        return self.__disponible and self.__precio_hora > 0  # devuelve un valor al llamador

    @abstractmethod  # aplica un decorador al siguiente metodo
    def describir(self) -> str:  # define la funcion o metodo describir
        pass  # mantiene el bloque sin instrucciones adicionales

    @abstractmethod  # aplica un decorador al siguiente metodo
    def tipo_servicio(self) -> str:  # define la funcion o metodo tipo_servicio
        pass  # mantiene el bloque sin instrucciones adicionales

    def __str__(self):  # define la funcion o metodo __str__
        return self.describir()  # devuelve un valor al llamador


# =============================================================
# SERVICIO 1: RESERVA DE SALA
# =============================================================

class ReservaSala(Servicio):  # define la clase ReservaSala
    """Servicio de reserva de salas de reunión o conferencia."""

    PRECIO_HORA_BASE = 50_000  # COP

    def __init__(self, id_servicio: str, nombre: str, capacidad: int):  # define la funcion o metodo __init__
        if capacidad <= 0:  # evalua una condicion para decidir el flujo
            raise ServicioNoDisponibleError(  # lanza una excepcion con un mensaje
                f"La capacidad de la sala debe ser mayor a 0. Recibido: {capacidad}"  # ejecuta esta instruccion del programa
            )  # cierra la llamada o estructura anterior
        # Precio varía según capacidad
        precio = self.PRECIO_HORA_BASE + (capacidad * 1_000)  # asigna o actualiza el valor de precio
        super().__init__(id_servicio, nombre, precio)  # inicializa la clase padre
        self.__capacidad = capacidad  # asigna o actualiza el valor de capacidad

    def get_capacidad(self) -> int:  # define la funcion o metodo get_capacidad
        return self.__capacidad  # devuelve un valor al llamador

    def tipo_servicio(self) -> str:  # define la funcion o metodo tipo_servicio
        return "Reserva de Sala"  # devuelve un valor al llamador

    def describir(self) -> str:  # define la funcion o metodo describir
        return (f"ReservaSala[{self.get_id()}] | {self.get_nombre()} | "  # devuelve un valor al llamador
                f"Capacidad: {self.__capacidad} personas | "  # ejecuta esta instruccion del programa
                f"Precio/hora: ${self.get_precio_hora():,.0f} COP")  # ejecuta esta instruccion del programa

    def calcular_costo(self, horas: int, con_iva: bool = False, descuento: float = 0.0) -> float:  # define la funcion o metodo calcular_costo
        """Sobrescribe calcular_costo agregando recargo por horas nocturnas si aplica."""
        costo = super().calcular_costo(horas, con_iva, descuento)  # asigna o actualiza el valor de costo
        return costo  # devuelve un valor al llamador


# =============================================================
# SERVICIO 2: ALQUILER DE EQUIPO
# =============================================================

class AlquilerEquipo(Servicio):  # define la clase AlquilerEquipo
    """Servicio de alquiler de equipos tecnológicos."""

    PRECIOS = {  # asigna o actualiza el valor de PRECIOS
        "laptop": 30_000,  # continua una llamada o estructura de datos
        "proyector": 20_000,  # continua una llamada o estructura de datos
        "impresora": 15_000,  # continua una llamada o estructura de datos
        "otro": 10_000  # ejecuta esta instruccion del programa
    }  # cierra la llamada o estructura anterior

    def __init__(self, id_servicio: str, nombre: str, tipo_equipo: str):  # define la funcion o metodo __init__
        tipo = tipo_equipo.lower().strip()  # asigna o actualiza el valor de tipo
        if tipo not in self.PRECIOS:  # evalua una condicion para decidir el flujo
            raise ServicioNoDisponibleError(  # lanza una excepcion con un mensaje
                f"Tipo de equipo '{tipo_equipo}' no válido. Opciones: {list(self.PRECIOS.keys())}"  # ejecuta esta instruccion del programa
            )  # cierra la llamada o estructura anterior
        precio = self.PRECIOS[tipo]  # asigna o actualiza el valor de precio
        super().__init__(id_servicio, nombre, precio)  # inicializa la clase padre
        self.__tipo_equipo = tipo  # asigna o actualiza el valor de tipo equipo

    def get_tipo_equipo(self) -> str:  # define la funcion o metodo get_tipo_equipo
        return self.__tipo_equipo  # devuelve un valor al llamador

    def tipo_servicio(self) -> str:  # define la funcion o metodo tipo_servicio
        return "Alquiler de Equipo"  # devuelve un valor al llamador

    def describir(self) -> str:  # define la funcion o metodo describir
        return (f"AlquilerEquipo[{self.get_id()}] | {self.get_nombre()} | "  # devuelve un valor al llamador
                f"Tipo: {self.__tipo_equipo} | "  # ejecuta esta instruccion del programa
                f"Precio/hora: ${self.get_precio_hora():,.0f} COP")  # ejecuta esta instruccion del programa

    def calcular_costo(self, horas: int, con_iva: bool = False, descuento: float = 0.0) -> float:  # define la funcion o metodo calcular_costo
        """Sobrescribe calcular_costo con recargo por uso extendido (>8 horas)."""
        costo = super().calcular_costo(horas, con_iva, descuento)  # asigna o actualiza el valor de costo
        if horas > 8:  # evalua una condicion para decidir el flujo
            recargo = costo * 0.05  # 5% recargo uso extendido
            costo += recargo  # asigna o actualiza el valor de costo
        return round(costo, 2)  # devuelve un valor al llamador


# =============================================================
# SERVICIO 3: ASESORÍA ESPECIALIZADA
# =============================================================

class AsesoriaEspecializada(Servicio):  # define la clase AsesoriaEspecializada
    """Servicio de asesoría técnica especializada."""

    PRECIO_HORA_BASE = 80_000  # COP

    ESPECIALIDADES_VALIDAS = [  # asigna o actualiza el valor de ESPECIALIDADES VALIDAS
        "python", "java", "bases de datos", "redes",  # continua una llamada o estructura de datos
        "seguridad", "machine learning", "web", "movil"  # ejecuta esta instruccion del programa
    ]  # cierra la llamada o estructura anterior

    def __init__(self, id_servicio: str, nombre: str, especialidad: str):  # define la funcion o metodo __init__
        esp = especialidad.lower().strip()  # asigna o actualiza el valor de esp
        if esp not in self.ESPECIALIDADES_VALIDAS:  # evalua una condicion para decidir el flujo
            raise ServicioNoDisponibleError(  # lanza una excepcion con un mensaje
                f"Especialidad '{especialidad}' no disponible. "  # ejecuta esta instruccion del programa
                f"Opciones: {self.ESPECIALIDADES_VALIDAS}"  # ejecuta esta instruccion del programa
            )  # cierra la llamada o estructura anterior
        super().__init__(id_servicio, nombre, self.PRECIO_HORA_BASE)  # inicializa la clase padre
        self.__especialidad = esp  # asigna o actualiza el valor de especialidad

    def get_especialidad(self) -> str:  # define la funcion o metodo get_especialidad
        return self.__especialidad  # devuelve un valor al llamador

    def tipo_servicio(self) -> str:  # define la funcion o metodo tipo_servicio
        return "Asesoría Especializada"  # devuelve un valor al llamador

    def describir(self) -> str:  # define la funcion o metodo describir
        return (f"AsesoriaEspecializada[{self.get_id()}] | {self.get_nombre()} | "  # devuelve un valor al llamador
                f"Especialidad: {self.__especialidad} | "  # ejecuta esta instruccion del programa
                f"Precio/hora: ${self.get_precio_hora():,.0f} COP")  # ejecuta esta instruccion del programa

    def calcular_costo(self, horas: int, con_iva: bool = False, descuento: float = 0.0) -> float:  # define la funcion o metodo calcular_costo
        """Sobrescribe calcular_costo con descuento automático por 5+ horas."""
        if horas >= 5:  # evalua una condicion para decidir el flujo
            descuento = max(descuento, 0.10)  # mínimo 10% descuento por volumen
        costo = super().calcular_costo(horas, con_iva, descuento)  # asigna o actualiza el valor de costo
        return costo  # devuelve un valor al llamador

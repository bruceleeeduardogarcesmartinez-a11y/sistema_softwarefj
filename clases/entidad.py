# =============================================================
# CLASE ABSTRACTA BASE - ENTIDAD
# Representa cualquier entidad general del sistema Software FJ
# =============================================================

from abc import ABC, abstractmethod  # importa elementos necesarios desde otro modulo


class Entidad(ABC):  # define la clase Entidad
    """
    Clase abstracta base. Todas las entidades del sistema
    (Cliente, Servicio, Reserva) heredan de esta clase.
    """

    def __init__(self, id_entidad: str):  # define la funcion o metodo __init__
        if not id_entidad or not isinstance(id_entidad, str):  # evalua una condicion para decidir el flujo
            raise ValueError("El ID de la entidad no puede estar vacío.")  # lanza una excepcion con un mensaje
        self.__id = id_entidad.strip()  # asigna o actualiza el valor de id

    def get_id(self) -> str:  # define la funcion o metodo get_id
        """Retorna el identificador único de la entidad."""
        return self.__id  # devuelve un valor al llamador

    @abstractmethod  # aplica un decorador al siguiente metodo
    def describir(self) -> str:  # define la funcion o metodo describir
        """Cada entidad debe implementar su propia descripción."""
        pass  # mantiene el bloque sin instrucciones adicionales

    @abstractmethod  # aplica un decorador al siguiente metodo
    def validar(self) -> bool:  # define la funcion o metodo validar
        """Cada entidad debe implementar su propia validación."""
        pass  # mantiene el bloque sin instrucciones adicionales

    def __repr__(self):  # define la funcion o metodo __repr__
        return self.describir()  # devuelve un valor al llamador

# =============================================================
# EXCEPCIONES PERSONALIZADAS - SOFTWARE FJ
# =============================================================

class SistemaError(Exception):  # define la clase SistemaError
    """Excepción base del sistema. Todas las excepciones heredan de esta."""
    def __init__(self, mensaje):  # define la funcion o metodo __init__
        super().__init__(mensaje)  # inicializa la clase padre
        self.mensaje = mensaje  # asigna o actualiza el valor de mensaje

    def __str__(self):  # define la funcion o metodo __str__
        return f"[{self.__class__.__name__}] {self.mensaje}"  # devuelve un valor al llamador


class ClienteInvalidoError(SistemaError):  # define la clase ClienteInvalidoError
    """Se lanza cuando los datos del cliente no son válidos."""
    pass  # mantiene el bloque sin instrucciones adicionales


class ServicioNoDisponibleError(SistemaError):  # define la clase ServicioNoDisponibleError
    """Se lanza cuando un servicio tiene parámetros inválidos o no está disponible."""
    pass  # mantiene el bloque sin instrucciones adicionales


class ReservaInvalidaError(SistemaError):  # define la clase ReservaInvalidaError
    """Se lanza cuando una reserva no puede ser creada o procesada."""
    pass  # mantiene el bloque sin instrucciones adicionales


class LogError(SistemaError):  # define la clase LogError
    """Se lanza cuando hay un error al escribir en el archivo de logs."""
    pass  # mantiene el bloque sin instrucciones adicionales

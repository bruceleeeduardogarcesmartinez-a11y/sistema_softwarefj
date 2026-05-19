# Sistema Integral de Gestión - Software FJ  
Curso: Programación 

Nombre: Brucelee Eduardo Garces Martinez

---

## Descripción
Sistema orientado a objetos que gestiona clientes, servicios y reservas para la empresa **Software FJ**, sin uso de bases de datos. Toda la información se maneja en memoria con objetos y listas.

## Estructura del proyecto
```
sistema_softwarefj/
│
├── main.py                  ← Punto de entrada, simula 10 operaciones
│
├── clases/
│   ├── entidad.py           ← Clase abstracta base (Entidad)
│   ├── cliente.py           ← Clase Cliente con encapsulación
│   ├── servicios.py         ← Servicio (abstracta) + ReservaSala, AlquilerEquipo, AsesoriaEspecializada
│   ├── reserva.py           ← Clase Reserva (integra cliente + servicio)
│   └── excepciones.py       ← Excepciones personalizadas del sistema
│
├── utils/
│   └── logger.py            ← Registro de eventos y errores en archivo
│
└── logs/
    └── sistema.log          ← Generado automáticamente al ejecutar
```

## Cómo ejecutar
```bash
python main.py
```

## Conceptos POO aplicados
| Concepto | Dónde se aplica |
|---|---|
| Abstracción | Clases `Entidad` y `Servicio` (ABC) |
| Herencia | `Cliente`, `ReservaSala`, etc. heredan de clases abstractas |
| Polimorfismo | `calcular_costo()` sobrescrito en cada servicio |
| Encapsulación | Atributos privados (`__nombre`) con getters/setters |
| Excepciones personalizadas | `ClienteInvalidoError`, `ServicioNoDisponibleError`, `ReservaInvalidaError` |
| try/except/else/finally | Aplicado en las 10 operaciones de `main.py` |
| Encadenamiento de excepciones | Operación 10 con `raise X from Y` |
| Archivo de logs | `utils/logger.py` → `logs/sistema.log` |

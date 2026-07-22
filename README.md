# API REST de Inventario con Flask

Laboratorio para desarrollar una API REST de inventario y ejecutar pruebas de rendimiento con Apache JMeter, k6 y pruebas basicas de seguridad con Python.

## Requisitos

- Python 3.11+
- uv
- Apache JMeter 5.x
- k6

## Instalacion

```bash
uv sync
```

## Ejecutar la API

```bash
uv run flask --app app run --host 0.0.0.0 --port 5000
```

La base de datos SQLite se crea automaticamente en `inventory.db`.

## Endpoints

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| GET | `/health` | Verifica que la API esta activa |
| GET | `/productos` | Lista productos |
| POST | `/productos` | Crea un producto |
| GET | `/productos/<id>` | Obtiene un producto |
| PUT | `/productos/<id>` | Actualiza un producto |
| DELETE | `/productos/<id>` | Elimina un producto |

Ejemplo de producto:

```json
{
  "nombre": "Monitor",
  "precio": 850.5,
  "cantidad": 12
}
```

## Pruebas de seguridad

Con la API en ejecucion:

```bash
uv run python security_tests.py
```

## Pruebas con k6

```bash
k6 run k6/inventory_load_test.js
```

Para apuntar a otra URL:

```bash
BASE_URL=http://127.0.0.1:5000 k6 run k6/inventory_load_test.js
```

## Pruebas con Apache JMeter

Abrir `jmeter/inventory_test_plan.jmx` desde JMeter. El plan incluye:

- Escenario 1: 20 usuarios, Ramp-Up 10 segundos, 5 iteraciones.
- Escenario 2: 50 usuarios, Ramp-Up 20 segundos, 10 iteraciones.
- Escenario 3: 100 usuarios, Ramp-Up 30 segundos, 15 iteraciones.
- Summary Report, Aggregate Report y Graph Results.

Tambien puede ejecutarse por consola:

```bash
mkdir -p results
jmeter -n -t jmeter/inventory_test_plan.jmx -l results/jmeter-results.jtl
```

## Capturas requeridas

Tomar capturas en JMeter de:

- Test Plan.
- Thread Group.
- HTTP Request.
- Summary Report.
- Aggregate Report.
- Graph Results.

## Informe

Completar `docs/informe-tecnico.md` con las metricas reales obtenidas en la maquina donde se ejecuten las pruebas.

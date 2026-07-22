# Informe tecnico: API REST de Inventario con Flask

## Datos generales

| Campo | Detalle |
| --- | --- |
| Proyecto | API REST de Inventario |
| Lenguaje | Python |
| Framework | Flask |
| Gestor de entorno | uv |
| Persistencia | SQLite |
| Pruebas de rendimiento | Apache JMeter y k6 |
| Pruebas de seguridad | Python Requests |

## Resumen de ejecucion

La API REST fue implementada con Flask y utiliza SQLite para almacenar productos de inventario. Se implementaron servicios REST `GET`, `POST`, `PUT` y `DELETE` sobre el recurso `/productos`.

En esta maquina se ejecutaron las pruebas automaticas disponibles con Python y Flask. Apache JMeter y k6 no se pudieron ejecutar localmente porque no estan instalados en el `PATH`, por lo tanto este informe incluye el procedimiento exacto para instalarlos, ejecutarlos, capturar evidencia y completar las tablas de resultados.

## Estructura del proyecto entregado

| Archivo | Descripcion |
| --- | --- |
| `app.py` | API REST de inventario con Flask y SQLite |
| `pyproject.toml` | Dependencias y configuracion del proyecto con uv |
| `uv.lock` | Versiones bloqueadas de dependencias |
| `security_tests.py` | Programa Python con pruebas basicas de seguridad |
| `jmeter/inventory_test_plan.jmx` | Plan de pruebas para Apache JMeter |
| `k6/inventory_load_test.js` | Script de pruebas de rendimiento con k6 |
| `README.md` | Guia rapida de instalacion y ejecucion |
| `Informe.md` | Informe tecnico y guia de entrega |

## Ejercicio 1. Desarrollo de una API REST

### Objetivo

Desarrollar una API REST utilizando Python y Flask para un sistema de inventario. La API permite listar, crear, consultar, actualizar y eliminar productos.

### Modelo de datos

Cada producto tiene la siguiente estructura:

```json
{
  "id": 1,
  "nombre": "Laptop",
  "precio": 3500.0,
  "cantidad": 10
}
```

### Endpoints implementados

| Metodo | Endpoint | Descripcion | Respuesta esperada |
| --- | --- | --- | --- |
| `GET` | `/health` | Verifica que la API esta activa | `200 OK` |
| `GET` | `/productos` | Lista todos los productos | `200 OK` |
| `POST` | `/productos` | Crea un nuevo producto | `201 Created` |
| `GET` | `/productos/<id>` | Obtiene un producto por ID | `200 OK` o `404 Not Found` |
| `PUT` | `/productos/<id>` | Actualiza un producto por ID | `200 OK` o `404 Not Found` |
| `DELETE` | `/productos/<id>` | Elimina un producto por ID | `204 No Content` o `404 Not Found` |

### Validaciones implementadas

| Campo | Regla |
| --- | --- |
| `nombre` | Obligatorio, texto, no puede estar vacio |
| `precio` | Obligatorio, numerico, mayor o igual a 0 |
| `cantidad` | Obligatorio, entero, mayor o igual a 0 |

### Como instalar dependencias

Ejecutar en la raiz del proyecto:

```bash
uv sync
```

### Como levantar la API

Ejecutar:

```bash
uv run flask --app app run --host 0.0.0.0 --port 5000
```

La API queda disponible en:

```text
http://127.0.0.1:5000
```

### Verificacion ejecutada

Se verifico el CRUD completo usando el cliente de pruebas de Flask:

```bash
uv run python -c "from app import app; c=app.test_client(); assert c.get('/productos').status_code == 200; r=c.post('/productos', json={'nombre':'Monitor','precio':850,'cantidad':3}); assert r.status_code == 201; product_id=r.get_json()['id']; assert c.get(f'/productos/{product_id}').status_code == 200; assert c.put(f'/productos/{product_id}', json={'nombre':'Monitor 2','precio':900,'cantidad':4}).status_code == 200; assert c.delete(f'/productos/{product_id}').status_code == 204; assert c.get(f'/productos/{product_id}').status_code == 404; print('CRUD OK')"
```

Resultado obtenido:

```text
CRUD OK
```

## Ejercicio 2. Pruebas de rendimiento con Apache JMeter

### Archivo entregado

El plan de pruebas se encuentra en:

```text
jmeter/inventory_test_plan.jmx
```

### Instalacion de JMeter

Si no esta instalado, descargar Apache JMeter desde:

```text
https://jmeter.apache.org/download_jmeter.cgi
```

Luego descomprimirlo y ejecutar:

```bash
./bin/jmeter
```

En Windows se puede abrir:

```text
bin/jmeter.bat
```

### Preparacion antes de ejecutar JMeter

Primero levantar la API:

```bash
uv run flask --app app run --host 0.0.0.0 --port 5000
```

Confirmar que responde:

```bash
curl http://127.0.0.1:5000/health
```

Respuesta esperada:

```json
{"status":"ok"}
```

### Como abrir el plan en JMeter

1. Abrir Apache JMeter.
2. Ir a `File` > `Open`.
3. Seleccionar `jmeter/inventory_test_plan.jmx`.
4. Verificar las variables del Test Plan:

| Variable | Valor |
| --- | --- |
| `HOST` | `127.0.0.1` |
| `PORT` | `5000` |

### Escenarios configurados

| Escenario | Usuarios concurrentes | Ramp-Up | Iteraciones |
| --- | ---: | ---: | ---: |
| Escenario 1 | 20 | 10 segundos | 5 |
| Escenario 2 | 50 | 20 segundos | 10 |
| Escenario 3 | 100 | 30 segundos | 15 |

### Que capturas tomar en JMeter

El laboratorio solicita adjuntar capturas. Tomar capturas de estas pantallas:

| Captura requerida | Donde encontrarla |
| --- | --- |
| Test Plan | Nodo principal `API Inventario - Plan de Rendimiento` |
| Thread Group | Cada escenario: `Escenario 1`, `Escenario 2`, `Escenario 3` |
| HTTP Request | Nodo `GET /productos` dentro de cada escenario |
| Summary Report | Listener `Summary Report` |
| Aggregate Report | Listener `Aggregate Report` |
| Graph Results | Listener `Graph Results` |

### Como ejecutar desde la interfaz grafica

1. Abrir el archivo `.jmx`.
2. Verificar que la API este corriendo.
3. Presionar el boton verde `Start`.
4. Esperar a que finalicen los tres escenarios.
5. Revisar `Summary Report` y `Aggregate Report`.
6. Copiar los valores a la tabla de resultados.
7. Tomar las capturas solicitadas.

### Como ejecutar desde consola

Crear carpeta de resultados:

```bash
mkdir -p results
```

Ejecutar JMeter en modo no grafico:

```bash
jmeter -n -t jmeter/inventory_test_plan.jmx -l results/jmeter-results.jtl
```

Generar reporte HTML opcional:

```bash
jmeter -g results/jmeter-results.jtl -o results/jmeter-html-report
```

### Metricas que se deben registrar

Las metricas salen principalmente de `Summary Report` y `Aggregate Report`.

| Metrica solicitada | Nombre comun en JMeter |
| --- | --- |
| Tiempo promedio de respuesta | `Average` |
| Tiempo minimo | `Min` |
| Tiempo maximo | `Max` |
| Throughput | `Throughput` |
| Error Rate | `Error %` |
| Desviacion estandar | `Std. Dev.` |

### Resultados Apache JMeter

Completar esta tabla despues de ejecutar JMeter:

| Escenario | Usuarios | Ramp-Up | Iteraciones | Promedio | Minimo | Maximo | Throughput | Error Rate | Desviacion estandar |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 20 | 10 s | 5 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 2 | 50 | 20 s | 10 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 3 | 100 | 30 s | 15 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

### Analisis esperado para JMeter

Al aumentar la cantidad de usuarios concurrentes, normalmente se observa un aumento del tiempo promedio de respuesta. Si el servidor Flask de desarrollo o SQLite empiezan a saturarse, puede aumentar la desviacion estandar y aparecer porcentaje de error.

## Ejercicio 3. Pruebas de rendimiento utilizando k6

### Archivo entregado

El script de k6 se encuentra en:

```text
k6/inventory_load_test.js
```

### Instalacion de k6

En Ubuntu/Debian, instalar segun la documentacion oficial:

```text
https://grafana.com/docs/k6/latest/set-up/install-k6/
```

Verificar instalacion:

```bash
k6 version
```

### Preparacion antes de ejecutar k6

Levantar la API:

```bash
uv run flask --app app run --host 0.0.0.0 --port 5000
```

Ejecutar k6 en otra terminal:

```bash
k6 run k6/inventory_load_test.js
```

Si se necesita cambiar la URL base:

```bash
BASE_URL=http://127.0.0.1:5000 k6 run k6/inventory_load_test.js
```

### Escenarios configurados en k6

| Escenario | Usuarios virtuales | Duracion |
| --- | ---: | ---: |
| 1 | 20 | 30 segundos |
| 2 | 50 | 45 segundos |
| 3 | 100 | 60 segundos |

### Que hace el script de k6

Cada usuario virtual ejecuta operaciones sobre la API:

| Operacion | Endpoint | Codigo esperado |
| --- | --- | ---: |
| Listar productos | `GET /productos` | 200 |
| Crear producto | `POST /productos` | 201 |
| Obtener producto | `GET /productos/<id>` | 200 |
| Actualizar producto | `PUT /productos/<id>` | 200 |
| Eliminar producto | `DELETE /productos/<id>` | 204 |

### Metricas que se deben registrar desde k6

Al finalizar, k6 imprime un resumen en consola. Copiar estas metricas:

| Metrica solicitada | Nombre comun en k6 |
| --- | --- |
| Iteraciones ejecutadas | `iterations` |
| Tiempo promedio de respuesta | `http_req_duration avg` |
| Tiempo maximo de respuesta | `http_req_duration max` |
| Throughput | `http_reqs` por segundo |
| Solicitudes exitosas | `successful_requests` |
| Solicitudes fallidas | `failed_requests` |
| Porcentaje de errores | `http_req_failed` o `error_rate` |

### Resultados k6

Completar esta tabla despues de ejecutar k6:

| Escenario | VUs | Duracion | Iteraciones | Promedio | Maximo | Throughput | Exitosas | Fallidas | Error Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 20 | 30 s | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 2 | 50 | 45 s | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 3 | 100 | 60 s | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

### Interpretacion esperada para k6

k6 suele mostrar claramente el tiempo promedio, percentiles, tasa de errores y cantidad total de solicitudes. A diferencia de JMeter, k6 se ejecuta principalmente desde consola y es mas facil de automatizar en pipelines.

## Ejercicio 4. Pruebas basicas de seguridad utilizando Python

### Archivo entregado

El programa se encuentra en:

```text
security_tests.py
```

### Como ejecutar las pruebas de seguridad

Primero levantar la API:

```bash
uv run flask --app app run --host 0.0.0.0 --port 5000
```

En otra terminal ejecutar:

```bash
uv run python security_tests.py
```

### Casos evaluados

| Caso | Solicitud | Resultado esperado |
| --- | --- | --- |
| Caso 1. Recurso inexistente | `GET /productos/999999` | HTTP 404 |
| Caso 2. Datos incompletos | `POST /productos` con campos faltantes o vacios | HTTP 400 y mensaje descriptivo |
| Caso 3. Tipos de datos incorrectos | `nombre` numerico, `precio` texto | HTTP 400 |
| Caso 4. Metodo no permitido | `PATCH /productos` | HTTP 405 |
| Caso 5. Fuerza bruta | No aplica | La API no implementa autenticacion |

### Resultado ejecutado

Resultado obtenido al ejecutar `security_tests.py` contra la API local:

```text
[PASS] GET recurso inexistente -> HTTP 404
[PASS] POST con datos incompletos -> HTTP 400
[PASS] POST con tipos invalidos -> HTTP 400
[PASS] Metodo HTTP no permitido -> HTTP 405
```

### Tabla de seguridad

| Caso | Entrada | Resultado esperado | Resultado obtenido |
| --- | --- | --- | --- |
| Recurso inexistente | `GET /productos/999999` | HTTP 404 | HTTP 404 - PASS |
| Datos incompletos | `POST /productos` con campos faltantes o vacios | HTTP 400 y mensaje descriptivo | HTTP 400 - PASS |
| Tipos invalidos | `nombre` numerico, `precio` texto | HTTP 400 | HTTP 400 - PASS |
| Metodo no permitido | `PATCH /productos` | HTTP 405 | HTTP 405 - PASS |
| Fuerza bruta | Intentos de login incorrectos | Opcional si hay autenticacion | No aplica, la API no tiene autenticacion |

## Comparacion entre JMeter y k6

Completar despues de ejecutar ambas herramientas:

| Criterio | Apache JMeter | k6 |
| --- | --- | --- |
| Forma de ejecucion | GUI y consola | Consola |
| Facilidad para capturas | Alta, por la interfaz grafica | Media, requiere capturar consola o exportar resultados |
| Automatizacion | Posible, pero mas pesada | Alta, orientada a scripts |
| Lectura de resultados | Summary Report, Aggregate Report, Graph Results | Resumen en consola con metricas HTTP |
| Throughput mayor observado | Pendiente | Pendiente |
| Error Rate observado | Pendiente | Pendiente |

## Tabla comparativa final de carga

Completar esta tabla con los resultados reales:

| Escenario | Usuarios | Promedio JMeter | Throughput JMeter | Error Rate JMeter | Promedio k6 | Throughput k6 | Error Rate k6 | Analisis |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 20 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Carga baja, se espera estabilidad |
| 2 | 50 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Carga media, se espera aumento de latencia |
| 3 | 100 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Carga alta, pueden aparecer errores o mayor variacion |

## Respuestas al analisis de resultados

### 1. Cual fue el tiempo promedio de respuesta de la API en cada escenario de carga?

Debe completarse con los valores reales de JMeter y k6. La API ya esta preparada para ejecutar los tres escenarios.

| Escenario | Promedio JMeter | Promedio k6 |
| --- | ---: | ---: |
| 1 | Pendiente | Pendiente |
| 2 | Pendiente | Pendiente |
| 3 | Pendiente | Pendiente |

### 2. Que herramienta presento mayor Throughput: Apache JMeter o k6?

Debe responderse comparando el campo `Throughput` de JMeter contra `http_reqs` por segundo de k6. En general, k6 puede obtener mejor throughput local por ser liviano y correr desde consola, pero la respuesta final debe basarse en los datos reales obtenidos.

### 3. En que escenario comenzaron a presentarse errores de respuesta?

Debe revisarse el campo `Error %` en JMeter y `http_req_failed` o `error_rate` en k6. Si todos los valores son 0%, se debe indicar que no se presentaron errores en los escenarios evaluados.

### 4. Que componente de la infraestructura representa el principal cuello de botella?

Para este laboratorio, los candidatos principales son:

- Servidor de desarrollo de Flask, porque no esta pensado para produccion ni alta concurrencia.
- SQLite, porque las escrituras concurrentes pueden bloquearse bajo carga alta.
- Recursos de la maquina local, especialmente CPU y memoria si JMeter, k6 y Flask corren en el mismo equipo.

### 5. Que recomendaciones implementaria para mejorar rendimiento y seguridad?

Recomendaciones:

- Ejecutar Flask con un servidor WSGI como Gunicorn o uWSGI para cargas reales.
- Usar una base de datos mas robusta para concurrencia, como PostgreSQL.
- Separar la maquina que genera carga de la maquina donde corre la API.
- Agregar autenticacion si la API fuera real.
- Agregar limitacion de tasa de solicitudes para reducir abuso.
- Registrar errores y eventos importantes.
- Desactivar `debug=True` en ambientes productivos.
- Validar siempre tipos de datos y campos obligatorios.
- Usar HTTPS en despliegues reales.

## Evidencias que deben adjuntarse

Adjuntar al documento final o presentacion:

- Captura del codigo fuente de la API.
- Captura de la API ejecutandose.
- Captura de `uv sync` o entorno instalado.
- Captura de JMeter Test Plan.
- Captura de cada Thread Group.
- Captura de HTTP Request.
- Captura de Summary Report.
- Captura de Aggregate Report.
- Captura de Graph Results.
- Captura de ejecucion de k6.
- Captura de ejecucion de `security_tests.py`.

## Conclusiones

La API REST de inventario cumple con los servicios minimos solicitados: `GET`, `POST`, `PUT` y `DELETE`. La persistencia con SQLite permite mantener datos entre ejecuciones y representa un escenario mas realista que el almacenamiento en memoria.

Las pruebas basicas de seguridad fueron ejecutadas correctamente y validaron respuestas esperadas para recursos inexistentes, datos incompletos, tipos invalidos y metodos HTTP no permitidos.

Las pruebas de rendimiento con JMeter y k6 quedaron implementadas mediante archivos entregables. Para completar el analisis final, se deben ejecutar en una maquina con JMeter y k6 instalados, registrar las metricas solicitadas y adjuntar las capturas de pantalla requeridas.

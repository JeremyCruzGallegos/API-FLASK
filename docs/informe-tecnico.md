# Informe tecnico: API REST de Inventario

## Objetivo

Evaluar el comportamiento de una API REST desarrollada con Flask bajo distintos niveles de carga usando Apache JMeter y k6, y validar controles basicos de seguridad con Python Requests.

## Arquitectura

- Framework: Flask.
- Gestor de dependencias: uv.
- Persistencia: SQLite.
- Recurso principal: productos de inventario.
- Endpoints implementados: GET, POST, PUT y DELETE.

## Resultados Apache JMeter

| Escenario | Usuarios | Ramp-Up | Iteraciones | Promedio | Minimo | Maximo | Throughput | Error Rate | Desviacion estandar |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 20 | 10 s | 5 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 2 | 50 | 20 s | 10 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 3 | 100 | 30 s | 15 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

## Resultados k6

| Escenario | VUs | Duracion | Iteraciones | Promedio | Maximo | Throughput | Exitosas | Fallidas | Error Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 20 | 30 s | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 2 | 50 | 45 s | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 3 | 100 | 60 s | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

## Pruebas basicas de seguridad

| Caso | Entrada | Resultado esperado | Resultado obtenido |
| --- | --- | --- | --- |
| Recurso inexistente | `GET /productos/999999` | HTTP 404 | Pendiente |
| Datos incompletos | `POST /productos` con campos faltantes o vacios | HTTP 400 y mensaje descriptivo | Pendiente |
| Tipos invalidos | `nombre` numerico, `precio` texto | HTTP 400 | Pendiente |
| Metodo no permitido | `PATCH /productos` | HTTP 405 | Pendiente |

## Analisis de resultados

1. Tiempo promedio de respuesta por escenario: completar con los valores de JMeter y k6.
2. Herramienta con mayor Throughput: comparar los resultados reales. k6 suele generar carga con menor consumo local; JMeter ofrece mas visualizacion desde GUI.
3. Escenario donde aparecen errores: completar segun Error Rate.
4. Posible cuello de botella: en este laboratorio probablemente SQLite y el servidor de desarrollo de Flask, especialmente con escrituras concurrentes.
5. Recomendaciones: usar un servidor WSGI como Gunicorn, separar base de datos, agregar indices si crece el modelo, validar entradas, registrar eventos, limitar tasa de requests y no exponer `debug=True` en produccion.

## Conclusiones

Completar despues de ejecutar las pruebas y adjuntar las capturas solicitadas.

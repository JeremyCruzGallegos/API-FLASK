import argparse
import sys
import requests

def run_security_tests(base_url: str) -> int:
    session = requests.Session()
    failures = 0

    print("=" * 80)
    print("EJECUTANDO PRUEBAS BÁSICAS DE SEGURIDAD - API DE INVENTARIO")
    print("=" * 80)

    # Casos de prueba
    tests = [
        # CASO 1: Recursos inexistentes
        {
            "id": "CASO 1.1",
            "name": "GET a un ID de producto inexistente",
            "method": "GET",
            "url": f"{base_url}/productos/999999",
            "json": None,
            "expected_status": 404,
            "description": "Verifica que la API retorne HTTP 404 Not Found al buscar un ID de producto inexistente."
        },
        
        # CASO 2: Datos incompletos
        {
            "id": "CASO 2.1",
            "name": "POST con campo 'nombre' faltante",
            "method": "POST",
            "url": f"{base_url}/productos",
            "json": {"precio": 120.5, "cantidad": 5},
            "expected_status": 400,
            "description": "Verifica que la API rechace la creación (HTTP 400) si falta el campo obligatorio 'nombre'."
        },
        {
            "id": "CASO 2.2",
            "name": "POST con campo 'nombre' vacío",
            "method": "POST",
            "url": f"{base_url}/productos",
            "json": {"nombre": "   ", "precio": 120.5, "cantidad": 5},
            "expected_status": 400,
            "description": "Verifica que la API rechace la creación (HTTP 400) si 'nombre' contiene solo espacios o está vacío."
        },
        {
            "id": "CASO 2.3",
            "name": "POST con campo 'precio' faltante",
            "method": "POST",
            "url": f"{base_url}/productos",
            "json": {"nombre": "Monitor", "cantidad": 5},
            "expected_status": 400,
            "description": "Verifica que la API rechace la creación (HTTP 400) si falta el campo obligatorio 'precio'."
        },
        {
            "id": "CASO 2.4",
            "name": "POST con campo 'cantidad' faltante",
            "method": "POST",
            "url": f"{base_url}/productos",
            "json": {"nombre": "Monitor", "precio": 450.0},
            "expected_status": 400,
            "description": "Verifica que la API rechace la creación (HTTP 400) si falta el campo obligatorio 'cantidad'."
        },

        # CASO 3: Tipos de datos incorrectos
        {
            "id": "CASO 3.1",
            "name": "POST con tipo inválido para 'nombre' (numérico)",
            "method": "POST",
            "url": f"{base_url}/productos",
            "json": {"nombre": 12345, "precio": 120.5, "cantidad": 5},
            "expected_status": 400,
            "description": "Verifica que la API rechace la petición (HTTP 400) si 'nombre' es un entero."
        },
        {
            "id": "CASO 3.2",
            "name": "POST con tipo inválido para 'precio' (texto)",
            "method": "POST",
            "url": f"{base_url}/productos",
            "json": {"nombre": "Mouse Gamer", "precio": "ABC", "cantidad": 5},
            "expected_status": 400,
            "description": "Verifica que la API rechace la petición (HTTP 400) si 'precio' es un string de texto."
        },
        {
            "id": "CASO 3.3",
            "name": "POST con tipo inválido para 'cantidad' (decimal/float)",
            "method": "POST",
            "url": f"{base_url}/productos",
            "json": {"nombre": "Mouse Gamer", "precio": 150.0, "cantidad": 10.5},
            "expected_status": 400,
            "description": "Verifica que la API rechace la petición (HTTP 400) si 'cantidad' es un decimal."
        },
        {
            "id": "CASO 3.4",
            "name": "POST con precio negativo",
            "method": "POST",
            "url": f"{base_url}/productos",
            "json": {"nombre": "Teclado", "precio": -50.0, "cantidad": 10},
            "expected_status": 400,
            "description": "Verifica que la API rechace la petición (HTTP 400) si el precio es inferior a 0."
        },

        # CASO 4: Método HTTP no permitido
        {
            "id": "CASO 4.1",
            "name": "PATCH a /productos (no soportado)",
            "method": "PATCH",
            "url": f"{base_url}/productos",
            "json": {"nombre": "Laptop Pro", "precio": 3500.0, "cantidad": 5},
            "expected_status": 405,
            "description": "Verifica que la API retorne HTTP 405 Method Not Allowed para PATCH en la colección /productos."
        },
        {
            "id": "CASO 4.2",
            "name": "PUT a /productos (no soportado en colección)",
            "method": "PUT",
            "url": f"{base_url}/productos",
            "json": {"nombre": "Laptop Pro", "precio": 3500.0, "cantidad": 5},
            "expected_status": 405,
            "description": "Verifica que la API retorne HTTP 405 Method Not Allowed para PUT en la colección /productos."
        }
    ]

    for check in tests:
        print("-" * 80)
        print(f"Prueba: {check['id']} - {check['name']}")
        print(f"Descripción: {check['description']}")
        print(f"Endpoint: {check['method']} {check['url']}")
        if check['json']:
            print(f"Payload: {check['json']}")
        else:
            print("Payload: Ninguno")
        
        try:
            response = session.request(
                check["method"],
                check["url"],
                json=check["json"],
                timeout=10
            )
            
            received_status = response.status_code
            expected_status = check["expected_status"]
            
            ok = received_status == expected_status
            status = "PASS" if ok else "FAIL"
            
            if not ok:
                failures += 1
                
            print(f"Código HTTP esperado: {expected_status}")
            print(f"Código HTTP recibido: {received_status}")
            print(f"Resultado: {status}")
            print(f"Respuesta del servidor: {response.text.strip()}")
            
        except Exception as e:
            failures += 1
            print(f"Resultado: FAIL (Error de conexión: {str(e)})")
            
    print("=" * 80)
    print("CASO 5: Fuerza Bruta")
    print("Descripción: Realizar múltiples intentos con credenciales incorrectas (si existe autenticación).")
    print("Resultado: OMITIDO (La API no implementa autenticación, sesiones ni login en ningún endpoint)")
    print("=" * 80)
    
    total_tests = len(tests)
    print(f"\nResumen final de pruebas: {total_tests} ejecutadas. Fallas: {failures}.")
    return failures

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pruebas automáticas de seguridad para la API de inventario")
    parser.add_argument("--base-url", default="http://127.0.0.1:5000", help="URL base de la API")
    args = parser.parse_args()
    
    sys.exit(run_security_tests(args.base_url.rstrip("/")))

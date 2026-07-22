import argparse

import requests


def run_security_tests(base_url: str) -> int:
    session = requests.Session()
    failures = 0

    checks = [
        {
            "name": "GET recurso inexistente",
            "method": "GET",
            "url": f"{base_url}/productos/999999",
            "expected_status": 404,
        },
        {
            "name": "POST con datos incompletos",
            "method": "POST",
            "url": f"{base_url}/productos",
            "json": {"nombre": "", "precio": 100},
            "expected_status": 400,
        },
        {
            "name": "POST con tipos invalidos",
            "method": "POST",
            "url": f"{base_url}/productos",
            "json": {"nombre": 12345, "precio": "ABC", "cantidad": "diez"},
            "expected_status": 400,
        },
        {
            "name": "Metodo HTTP no permitido",
            "method": "PATCH",
            "url": f"{base_url}/productos",
            "json": {"nombre": "Monitor", "precio": 900, "cantidad": 5},
            "expected_status": 405,
        },
    ]

    for check in checks:
        response = session.request(
            check["method"],
            check["url"],
            json=check.get("json"),
            timeout=10,
        )
        ok = response.status_code == check["expected_status"]
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {check['name']} -> HTTP {response.status_code}")
        if not ok:
            failures += 1
            print(f"  Esperado: HTTP {check['expected_status']}")
            print(f"  Respuesta: {response.text}")

    return failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pruebas basicas de seguridad para la API de inventario")
    parser.add_argument("--base-url", default="http://127.0.0.1:5000", help="URL base de la API")
    args = parser.parse_args()
    raise SystemExit(run_security_tests(args.base_url.rstrip("/")))

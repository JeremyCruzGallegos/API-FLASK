import os
import sqlite3
from pathlib import Path

from flask import Flask, g, jsonify, request


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(os.environ.get("DATABASE_PATH", BASE_DIR / "inventory.db"))


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    @app.before_request
    def ensure_database() -> None:
        init_database()

    @app.teardown_appcontext
    def close_database(error: Exception | None = None) -> None:
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Solicitud invalida"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Metodo HTTP no permitido"}), 405

    @app.get("/health")
    def health_check():
        return jsonify({"status": "ok"})

    @app.get("/productos")
    def list_products():
        rows = get_database().execute(
            "SELECT id, nombre, precio, cantidad FROM productos ORDER BY id"
        ).fetchall()
        return jsonify([serialize_product(row) for row in rows])

    @app.post("/productos")
    def create_product():
        payload = request.get_json(silent=True)
        data, error = validate_product_payload(payload, partial=False)
        if error:
            return jsonify({"error": error}), 400

        cursor = get_database().execute(
            "INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)",
            (data["nombre"], data["precio"], data["cantidad"]),
        )
        get_database().commit()
        product = find_product(cursor.lastrowid)
        return jsonify(serialize_product(product)), 201

    @app.get("/productos/<int:product_id>")
    def get_product(product_id: int):
        product = find_product(product_id)
        if product is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify(serialize_product(product))

    @app.put("/productos/<int:product_id>")
    def update_product(product_id: int):
        if find_product(product_id) is None:
            return jsonify({"error": "Producto no encontrado"}), 404

        payload = request.get_json(silent=True)
        data, error = validate_product_payload(payload, partial=False)
        if error:
            return jsonify({"error": error}), 400

        get_database().execute(
            """
            UPDATE productos
            SET nombre = ?, precio = ?, cantidad = ?
            WHERE id = ?
            """,
            (data["nombre"], data["precio"], data["cantidad"], product_id),
        )
        get_database().commit()
        return jsonify(serialize_product(find_product(product_id)))

    @app.delete("/productos/<int:product_id>")
    def delete_product(product_id: int):
        if find_product(product_id) is None:
            return jsonify({"error": "Producto no encontrado"}), 404

        get_database().execute("DELETE FROM productos WHERE id = ?", (product_id,))
        get_database().commit()
        return "", 204

    return app


def get_database() -> sqlite3.Connection:
    if "db" not in g:
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


def init_database() -> None:
    database_exists = DATABASE_PATH.exists()
    db = get_database()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL CHECK (precio >= 0),
            cantidad INTEGER NOT NULL CHECK (cantidad >= 0)
        )
        """
    )
    if not database_exists:
        db.executemany(
            "INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)",
            [
                ("Laptop", 3500.0, 10),
                ("Mouse", 90.0, 50),
                ("Teclado", 180.0, 25),
            ],
        )
    db.commit()


def find_product(product_id: int) -> sqlite3.Row | None:
    return get_database().execute(
        "SELECT id, nombre, precio, cantidad FROM productos WHERE id = ?",
        (product_id,),
    ).fetchone()


def serialize_product(product: sqlite3.Row | None) -> dict:
    return {
        "id": product["id"],
        "nombre": product["nombre"],
        "precio": product["precio"],
        "cantidad": product["cantidad"],
    }


def validate_product_payload(payload: dict | None, partial: bool = False) -> tuple[dict, str | None]:
    if not isinstance(payload, dict):
        return {}, "El cuerpo debe ser JSON valido"

    required_fields = ["nombre", "precio", "cantidad"]
    missing_fields = [field for field in required_fields if field not in payload]
    if missing_fields and not partial:
        return {}, f"Campos obligatorios faltantes: {', '.join(missing_fields)}"

    nombre = payload.get("nombre")
    precio = payload.get("precio")
    cantidad = payload.get("cantidad")

    if not isinstance(nombre, str) or not nombre.strip():
        return {}, "El campo nombre debe ser texto y no puede estar vacio"

    if not isinstance(precio, (int, float)) or isinstance(precio, bool) or precio < 0:
        return {}, "El campo precio debe ser numerico y mayor o igual a 0"

    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 0:
        return {}, "El campo cantidad debe ser entero y mayor o igual a 0"

    return {
        "nombre": nombre.strip(),
        "precio": float(precio),
        "cantidad": cantidad,
    }, None


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

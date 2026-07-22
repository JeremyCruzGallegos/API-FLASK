from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos en memoria
productos = [
    {"id": 1, "nombre": "Laptop", "precio": 3500},
    {"id": 2, "nombre": "Mouse", "precio": 90},
    {"id": 3, "nombre": "Teclado", "precio": 180}
]

# GET: Listar todos los productos
@app.route("/productos", methods=["GET"])
def listar():
    return jsonify(productos)

# POST: Registrar un nuevo producto
@app.route("/productos", methods=["POST"])
def registrar():
    datos = request.json
    nuevo = {
        "id": len(productos) + 1,
        "nombre": datos.get("nombre"),
        "precio": datos.get("precio")
    }
    productos.append(nuevo)
    return jsonify(nuevo), 201

# GET: Obtener un producto por ID
@app.route("/productos/<int:id>", methods=["GET"])
def obtener(id):
    for producto in productos:
        if producto["id"] == id:
            return jsonify(producto)
    return jsonify({"mensaje": "Producto no encontrado"}), 404

# PUT: Actualizar un producto por ID
@app.route("/productos/<int:id>", methods=["PUT"])
def actualizar(id):
    datos = request.json
    for producto in productos:
        if producto["id"] == id:
            producto["nombre"] = datos.get("nombre")
            producto["precio"] = datos.get("precio")
            return jsonify(producto)
    return jsonify({"mensaje": "Producto no encontrado"}), 404

# DELETE: Eliminar un producto por ID
@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar(id):
    global productos
    productos = [p for p in productos if p["id"] != id]
    return jsonify({"mensaje": "Producto eliminado"})

if __name__ == "__main__":
    app.run(debug=True)
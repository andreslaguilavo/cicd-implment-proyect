from flask import Blueprint, request, jsonify
from model.producto import Producto
from model.db import db

api = Blueprint("producto_api", __name__)

@api.route("/productos", methods=["GET"])
def list_productos():
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos])

@api.route("/productos/<int:pid>", methods=["GET"])
def get_producto(pid):
    p = Producto.query.get_or_404(pid)
    return jsonify(p.to_dict())

@api.route("/productos", methods=["POST"])
def create_producto():
    data = request.get_json(force=True, silent=True) or {}
    p = Producto(
        nombre=data.get("nombre", ""),
        descripcion=data.get("descripcion"),
        precio=data.get("precio", 0.0),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"mensaje": "Producto creado", "id": p.id}), 201

@api.route("/productos/<int:pid>", methods=["PUT"])
def update_producto(pid):
    data = request.get_json(force=True, silent=True) or {}
    p = Producto.query.get_or_404(pid)
    p.nombre = data.get("nombre", p.nombre)
    p.descripcion = data.get("descripcion", p.descripcion)
    p.precio = data.get("precio", p.precio)
    db.session.commit()
    return jsonify({"mensaje": "Producto actualizado"})

@api.route("/productos/<int:pid>", methods=["DELETE"])
def delete_producto(pid):
    p = Producto.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"mensaje": "Producto eliminado"})

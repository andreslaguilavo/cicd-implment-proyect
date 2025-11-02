from flask import Blueprint, request, jsonify
from model.Pedido import Pedido
from model.Producto import Producto
from model.Db import db

pedido_api = Blueprint('pedido_api', __name__)

@pedido_api.route('/pedidos', methods=['POST'])
def create_pedido():
    data = request.get_json(force=True, silent=True) or {}
    cliente_id = data.get("cliente_id")
    producto_ids = data.get("producto_ids", [])
    if not cliente_id:
        return jsonify({"error": "cliente_id es obligatorio"}), 400
    productos = Producto.query.filter(Producto.id.in_(producto_ids)).all() if producto_ids else []
    total = sum(p.precio for p in productos)
    ped = Pedido(cliente_id=cliente_id, productos=productos, total=total)
    db.session.add(ped)
    db.session.commit()
    return jsonify({"mensaje": "Pedido creado", "id": ped.id, "total": ped.total}), 201

@pedido_api.route('/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([
        {
            "id": p.id,
            "cliente_id": p.cliente_id,
            "total": p.total,
            "productos": [{"id": pr.id, "nombre": pr.nombre, "precio": pr.precio} for pr in p.productos]
        }
        for p in pedidos
    ])

@pedido_api.route('/pedidos/<int:id>', methods=['PUT'])
def update_pedido(id):
    ped = Pedido.query.get_or_404(id)
    data = request.get_json(force=True, silent=True) or {}
    if "cliente_id" in data:
        ped.cliente_id = data["cliente_id"]
    if "producto_ids" in data:
        productos = Producto.query.filter(Producto.id.in_(data["producto_ids"])).all()
        ped.productos = productos
        ped.total = sum(pr.precio for pr in productos)
    db.session.commit()
    return jsonify({"mensaje": "Pedido actualizado"})

@pedido_api.route('/pedidos/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    ped = Pedido.query.get_or_404(id)
    db.session.delete(ped)
    db.session.commit()
    return jsonify({"mensaje": "Pedido eliminado"})

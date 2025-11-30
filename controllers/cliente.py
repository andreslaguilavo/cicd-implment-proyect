from flask import Blueprint, request, jsonify
from model.cliente import Cliente
from model.db import db

cliente_api = Blueprint('cliente_api', __name__)


@cliente_api.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json(force=True, silent=True) or {}
    nombre = data.get("nombre")
    email = data.get("email")
    if not nombre:
        return jsonify({"error": "nombre es obligatorio"}), 400
    c = Cliente(nombre=nombre, email=email)
    db.session.add(c)
    db.session.commit()
    return jsonify({"mensaje": "Cliente creado", "id": c.id}), 201


@cliente_api.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([
        {"id": c.id, "nombre": c.nombre, "email": c.email}
        for c in clientes
    ])

# GET single cliente (int id)


@cliente_api.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    c = Cliente.query.get_or_404(id)
    return jsonify(c.to_dict())


@cliente_api.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    c = Cliente.query.get_or_404(id)
    data = request.get_json(force=True, silent=True) or {}
    c.nombre = data.get("nombre", c.nombre)
    c.email = data.get("email", c.email)
    db.session.commit()
    return jsonify({"mensaje": "Cliente actualizado"})


@cliente_api.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    c = Cliente.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"mensaje": "Cliente eliminado"})

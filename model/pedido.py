from .db import db

# association table for many-to-many Pedido <-> Producto
pedido_productos = db.Table(
    "pedido_productos",
    db.Column("pedido_id", db.Integer, db.ForeignKey(
        "pedidos.id"), primary_key=True),
    db.Column("producto_id", db.Integer, db.ForeignKey(
        "productos.id"), primary_key=True),
)


class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey(
        "clientes.id"), nullable=False)
    total = db.Column(db.Float, nullable=False, default=0.0)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    productos = db.relationship(
        "Producto", secondary=pedido_productos, back_populates="pedidos")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "total": self.total,
            "productos": [{"id": p.id, "nombre": p.nombre, "precio": p.precio} for p in self.productos]
        }

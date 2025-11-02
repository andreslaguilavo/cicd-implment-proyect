from .db import db

class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    cliente = db.relationship("Cliente", back_populates="pedidos")

    def to_dict(self):
        return {"id": self.id, "cliente_id": self.cliente_id}

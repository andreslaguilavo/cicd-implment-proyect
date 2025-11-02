from .db import db

class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)

    pedidos = db.relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "email": self.email}

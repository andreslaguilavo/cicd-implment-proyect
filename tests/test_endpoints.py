import pytest
from app import create_app, db
from model.Producto import Producto
from model.Cliente import Cliente
from model.Pedido import Pedido

class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    
@pytest.fixture(scope='session')
def app():
    _app = create_app(test_config=TestConfig)
    with _app.app_context():
        db.create_all()
    yield _app
    
@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        yield client

def test_create_producto(client):
    response = client.post('/api/productos', json={
        "nombre": "Test Producto",
        "descripcion": "Desc",
        "precio": 10.5
    })
    assert response.status_code == 201
    assert b"Producto creado" in response.data

def test_get_productos(client):
    client.post('/api/productos', json={
        "nombre": "Test Producto",
        "descripcion": "Desc",
        "precio": 10.5
    })
    response = client.get('/api/productos')
    assert response.status_code == 200
    assert b"Test Producto" in response.data

def test_create_cliente(client):
    response = client.post('/api/clientes', json={
        "nombre": "Cliente Uno",
        "email": "cliente@correo.com"
    })
    assert response.status_code == 201
    assert b"Cliente creado" in response.data

def test_create_pedido(client):
    client.post('/api/clientes', json={
        "nombre": "Cliente Uno",
        "email": "cliente@correo.com"
    })
    client.post('/api/productos', json={
        "nombre": "Test Producto",
        "descripcion": "Desc",
        "precio": 10.5
    })
    response = client.post('/api/pedidos', json={
        "cliente_id": 1,
        "producto_ids": [1]
    })
    assert response.status_code == 201
    assert b"Pedido creado" in response.data

def test_get_pedidos(client):
    client.post('/api/clientes', json={
        "nombre": "Cliente Uno",
        "email": "cliente@correo.com"
    })
    client.post('/api/productos', json={
        "nombre": "Test Producto",
        "descripcion": "Desc",
        "precio": 10.5
    })
    client.post('/api/pedidos', json={
        "cliente_id": 1,
        "producto_ids": [1]
    })
    response = client.get('/api/pedidos')
    assert response.status_code == 200
    assert b"Test Producto" in response.data
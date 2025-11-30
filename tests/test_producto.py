import pytest

BASE = "/api/productos"


def test_crud_producto_basic(client):
    # Create
    payload = {"nombre": "Lapicero",
               "descripcion": "Color azul", "precio": 2.5}
    r = client.post(BASE, json=payload)
    assert r.status_code == 201
    body = r.get_json()
    assert "id" in body
    pid = body["id"]

    # Get created
    r = client.get(f"{BASE}/{pid}")
    assert r.status_code == 200
    data = r.get_json()
    assert data["nombre"] == "Lapicero"
    assert data["precio"] == 2.5

    # List
    r = client.get(BASE)
    assert r.status_code == 200
    assert any(p["id"] == pid for p in r.get_json())

    # Update
    r = client.put(f"{BASE}/{pid}",
                   json={"nombre": "Lapicero Nuevo", "precio": 3.5})
    assert r.status_code == 200

    r = client.get(f"{BASE}/{pid}")
    assert r.get_json()["nombre"] == "Lapicero Nuevo"
    assert r.get_json()["precio"] == 3.5

    # Delete
    r = client.delete(f"{BASE}/{pid}")
    assert r.status_code == 200
    r = client.get(f"{BASE}/{pid}")
    assert r.status_code == 404


def test_create_producto_with_defaults(client):
    # Missing fields should create (API uses defaults)
    r = client.post(BASE, json={})
    assert r.status_code == 201
    body = r.get_json()
    assert "id" in body
    pid = body["id"]
    # Verify defaults: nombre empty, precio default 0.0
    r = client.get(f"{BASE}/{pid}")
    res = r.get_json()
    assert res["precio"] == 0.0

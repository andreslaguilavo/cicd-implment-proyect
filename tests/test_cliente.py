import pytest


def test_crud_cliente(client):
    # Create cliente (no id required)
    data = {"nombre": "Juan", "email": "juan@test.com"}
    r = client.post("/api/clientes", json=data)
    assert r.status_code == 201
    cid = r.get_json()["id"]

    # Get
    r = client.get(f"/api/clientes/{cid}")
    assert r.status_code == 200
    assert r.get_json()["nombre"] == "Juan"

    # List
    r = client.get("/api/clientes")
    assert r.status_code == 200
    assert any(c["id"] == cid for c in r.get_json())

    # Update
    r = client.put(f"/api/clientes/{cid}", json={"nombre": "Pedro"})
    assert r.status_code == 200
    r = client.get(f"/api/clientes/{cid}")
    assert r.get_json()["nombre"] == "Pedro"

    # Delete
    r = client.delete(f"/api/clientes/{cid}")
    assert r.status_code == 200
    r = client.get(f"/api/clientes/{cid}")
    assert r.status_code == 404

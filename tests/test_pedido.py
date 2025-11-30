import pytest

BASE = "/api/pedidos"
CLIENT_BASE = "/api/clientes"
PRODUCT_BASE = "/api/productos"


def test_crud_pedido_flow(client):
    # Create cliente
    cre = client.post(CLIENT_BASE, json={
                      "nombre": "Ana", "email": "ana@test.com"})
    assert cre.status_code == 201
    cid = cre.get_json()["id"]

    # Create product
    pr = client.post(PRODUCT_BASE, json={"nombre": "Lapiz", "precio": 1.5})
    assert pr.status_code == 201
    pid = pr.get_json()["id"]

    # Create pedido
    payload = {"cliente_id": cid, "producto_ids": [pid]}
    r = client.post(BASE, json=payload)
    assert r.status_code == 201
    body = r.get_json()
    assert "id" in body
    assert "total" in body
    assert body["total"] == 1.5
    ped_id = body["id"]

    # Get pedido
    r = client.get(f"{BASE}/{ped_id}")
    assert r.status_code == 200
    p = r.get_json()
    assert p["cliente_id"] == cid
    assert p["total"] == 1.5
    assert len(p["productos"]) == 1
    assert p["productos"][0]["id"] == pid

    # List pedidos
    r = client.get(BASE)
    assert r.status_code == 200
    assert any(item["id"] == ped_id for item in r.get_json())

    # Update pedido: change products to same product (test update path)
    r = client.put(f"{BASE}/{ped_id}", json={"producto_ids": [pid]})
    assert r.status_code == 200

    # Delete pedido
    r = client.delete(f"{BASE}/{ped_id}")
    assert r.status_code == 200
    r = client.get(f"{BASE}/{ped_id}")
    assert r.status_code == 404


def test_create_pedido_missing_fields(client):
    # missing cliente_id should return 400
    r = client.post(BASE, json={"producto_ids": []})
    assert r.status_code == 400

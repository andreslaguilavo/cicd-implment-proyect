import pytest


def test_error_handling(client):
    # Simula un error interno llamando a una ruta que lanza excepción
    @client.application.route("/error")
    def error():
        raise Exception("Test error")
    with pytest.raises(Exception):
        client.get("/error")

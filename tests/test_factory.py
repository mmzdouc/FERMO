from fermo_gui import create_app


def test_config_valid():
    assert create_app({"TESTING": True}).testing


def test_config_invalid():
    assert create_app().testing is False


def test_hello(client):
    response = client.get("/hello")
    assert response.data == b"Hello, World!"

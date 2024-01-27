import os

import pytest

from fermo_gui import (
    create_app,
    configure_app,
    create_instance_path,
)


def test_config_valid():
    assert create_app({"TESTING": True}).testing


def test_config_invalid():
    assert create_app().testing is False


def test_create_app_valid(app):
    assert app is not None


def test_configure_app_valid(app):
    configure_app(app, test_config={"TEST_KEY": "TEST_VALUE"})
    assert app.config["TEST_KEY"] == "TEST_VALUE"


def test_configure_app_invalid(app):
    configure_app(app)
    with pytest.raises(KeyError):
        assert app.config["TEST_KEY"] == "TEST_VALUE"


def test_create_instance_path(app):
    create_instance_path(app)
    assert os.path.exists(app.instance_path)


def test_register_blueprints_valid(client):
    response = client.get("/")
    assert response.status_code == 200

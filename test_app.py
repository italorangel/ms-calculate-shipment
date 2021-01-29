import pytest
from main import app as flask_app
import json


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_calculate_shipping_retuning_two_companies(client):
    product = {"dimensao": {"altura": 102, "largura": 40}, "peso": 400}
    expect = [{"nome": "Entrega Ninja", "valor_frete": 12.00, "prazo_dias": 6},
              {"nome": "Entrega KaBuM", "valor_frete": 8.00, "prazo_dias": 4}]
    res = client.post('/calculate-shipping', json=product)
    data = json.loads(res.get_data(as_text=True))
    assert res.status_code == 200
    assert expect == data


def test_calculate_shipping_retuning_one_company(client):
    product = {"dimensao": {"altura": 152, "largura": 50}, "peso": 850}
    expect = [{"nome": "Entrega Ninja", "valor_frete": 25.50, "prazo_dias": 6}]
    res = client.post('/calculate-shipping', json=product)
    data = json.loads(res.get_data(as_text=True))
    assert res.status_code == 200
    assert expect == data


def test_calculate_shipping_returning_none_companies(client):
    product = {"dimensao": {"altura": 230, "largura": 162}, "peso": 5600}
    expect = []
    res = client.post('/calculate-shipping', json=product)
    data = json.loads(res.get_data(as_text=True))
    assert res.status_code == 200
    assert expect == data

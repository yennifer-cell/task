import json
import pytest
from unittest.mock import patch

from app import app
import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_list(client):
    resp = client.get("/inventory")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)


def test_create_and_get_and_delete(client):
    # create
    payload = {"name": "Test Item", "price": 2.5, "stock": 5}
    r = client.post("/inventory", json=payload)
    assert r.status_code == 201
    item = r.get_json()
    iid = item["id"]

    # get
    r = client.get(f"/inventory/{iid}")
    assert r.status_code == 200

    # patch
    r = client.patch(f"/inventory/{iid}", json={"price": 3.0})
    assert r.status_code == 200
    assert r.get_json()["price"] == 3.0

    # delete
    r = client.delete(f"/inventory/{iid}")
    assert r.status_code == 200


def test_fetch_external_by_barcode(client):
    mock_resp = {"status": 1, "product": {"product_name": "Mocked"}}

    with patch("inventory.requests.get") as m:
        m.return_value.status_code = 200
        m.return_value.json.return_value = mock_resp
        r = client.get("/fetch", query_string={"q": "12345"})
        assert r.status_code == 200
        data = r.get_json()
        assert data.get("product_name") == "Mocked"


def test_fetch_external_by_name(client):
    mock_resp = {"products": [{"product_name": "Found"}]}
    with patch("inventory.requests.get") as m:
        m.return_value.status_code = 200
        m.return_value.json.return_value = mock_resp
        r = client.get("/fetch", query_string={"q": "Almond"})
        assert r.status_code == 200
        data = r.get_json()
        assert data.get("product_name") == "Found"

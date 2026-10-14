from fastapi.testclient import TestClient

from scout_ai.main import app
from scout_ai.rag.ingest import ingest_docs

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    assert "id" in data[0]


def test_list_products_filter_max_price():
    response = client.get("/products", params={"max_price": 1000})
    assert response.status_code == 200
    assert all(item["price_usd"] <= 1000 for item in response.json())


def test_get_product():
    response = client.get("/products/macbook-air-13-m4")
    assert response.status_code == 200
    assert response.json()["name"].startswith("MacBook Air")


def test_get_product_missing():
    response = client.get("/products/not-a-real-id")
    assert response.status_code == 404


def test_retrieve_endpoint():
    ingest_docs()
    response = client.get(
        "/retrieve",
        params={"query": "lightweight travel laptop battery life", "limit": 3},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["query"]
    assert body["citations"]
    assert "source" in body["citations"][0]
    assert "quote" in body["citations"][0]


def test_research_endpoint():
    ingest_docs()
    response = client.post(
        "/research",
        json={"question": "best laptop under $1000 for programming"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["top_pick"] is not None
    assert body["top_pick"]["price_usd"] <= 1000
    assert body["citations"]
    assert body["steps"]

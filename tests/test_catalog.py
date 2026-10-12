from scout_ai.catalog import get_product, load_products, search_products


def test_load_products_has_real_laptops():
    products = load_products()
    assert len(products) >= 5
    ids = {p.id for p in products}
    assert "macbook-air-13-m4" in ids


def test_get_product_found_and_missing():
    product = get_product("framework-13-amd")
    assert product is not None
    assert product.brand == "Framework"

    assert get_product("does-not-exist") is None


def test_search_by_max_price_and_tag():
    under_1000 = search_products(max_price=1000)
    assert under_1000
    assert all(p.price_usd <= 1000 for p in under_1000)

    programming = search_products(tag="programming")
    assert programming
    assert all("programming" in p.tags for p in programming)

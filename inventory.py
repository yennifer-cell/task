import requests

# Mock in-memory database
inventory_db = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 3.99,
        "stock": 20,
        "barcode": "000000000001",
    },
    {
        "id": 2,
        "name": "Granola Bar",
        "brand": "Nature's Path",
        "price": 1.5,
        "stock": 50,
        "barcode": "000000000002",
    },
]


def _next_id():
    if not inventory_db:
        return 1
    return max(i["id"] for i in inventory_db) + 1


def get_item(item_id):
    return next((i for i in inventory_db if i["id"] == item_id), None)


def add_item(data):
    item = {
        "id": _next_id(),
        "name": data.get("name"),
        "brand": data.get("brand"),
        "price": float(data.get("price", 0)),
        "stock": int(data.get("stock", 0)),
        "barcode": data.get("barcode"),
    }
    inventory_db.append(item)
    return item


def update_item(item_id, updates):
    item = get_item(item_id)
    if not item:
        return None
    for k, v in updates.items():
        if k in ["price"]:
            item[k] = float(v)
        elif k in ["stock"]:
            item[k] = int(v)
        else:
            item[k] = v
    return item


def delete_item(item_id):
    item = get_item(item_id)
    if not item:
        return False
    inventory_db.remove(item)
    return True


def fetch_external_product(q):
    """Query OpenFoodFacts by barcode (numeric) or name (text).

    Returns product dict or None.
    """
    if q.isdigit():
        url = f"https://world.openfoodfacts.org/api/v0/product/{q}.json"
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if data.get("status") != 1:
            return None
        return data.get("product")
    else:
        # search by name
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {"search_terms": q, "search_simple": 1, "json": 1}
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code != 200:
            return None
        data = resp.json()
        products = data.get("products", [])
        return products[0] if products else None

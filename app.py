from flask import Flask, jsonify, request, abort
from inventory import (
    inventory_db,
    get_item,
    add_item,
    update_item,
    delete_item,
    fetch_external_product,
)

app = Flask(__name__)


@app.route("/inventory", methods=["GET"])
def list_inventory():
    return jsonify(inventory_db)


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory(item_id):
    item = get_item(item_id)
    if not item:
        abort(404)
    return jsonify(item)


@app.route("/inventory", methods=["POST"])
def create_inventory():
    data = request.get_json()
    if not data or "name" not in data:
        abort(400)
    item = add_item(data)
    return jsonify(item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def patch_inventory(item_id):
    data = request.get_json()
    if not data:
        abort(400)
    item = update_item(item_id, data)
    if not item:
        abort(404)
    return jsonify(item)


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory(item_id):
    ok = delete_item(item_id)
    if not ok:
        abort(404)
    return jsonify({"deleted": item_id})


@app.route("/fetch", methods=["GET"])
def fetch_product():
    q = request.args.get("q")
    if not q:
        abort(400)
    result = fetch_external_product(q)
    if not result:
        return jsonify({"status": 0, "message": "not found"}), 404
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

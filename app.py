import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.get("/stores")
def get_all_stores():
    return {"stores": list(stores.values())}


@app.get("/stores/<string:store_id>")
def get_store(store_id):
    if store := stores.get(store_id):
        return store
    abort(404, message="Store not found.")


@app.post("/stores")
def create_stores():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
    for store in stores.values():
        if store.get("name") == store_data.get("name"):
            abort(400, message="Store already exist.")
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.delete("/stores/<string:store_id>")
def delete_store(store_id):
    if store := stores.get(store_id):
        del stores[store_id]
        return {"message": "Store deleted"}
    abort(404, message="Store not found.")


@app.get("/items")
def get_all_items():
    return {"items": list(items.values())}


@app.post("/items")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "name" not in item_data
        or "store_id" not in item_data
    ):
        abort(400, message="Bad request. Ensure 'price', 'name' and 'store_id are included in the JSON payload'")

    for item in items.values():
        if item.get("name") == item_data.get("name") and item.get("store_id") == item_data.get("store_id"):
            abort(400, message="Item already exist.")

    if item_data.get("store_id") not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/items/<string:item_id>")
def get_item(item_id):
    if item := items.get(item_id):
        return item
    abort(404, message="Item not found.")


@app.delete("/items/<string:item_id>")
def delete_item(item_id):
    if item := items.get(item_id):
        del items[item_id]
        return {"message": "Item deleted"}
    abort(404, message="Item not found.")


@app.put("/items/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "name" not in item_data or "price" not in item_data:
        abort(400, message="Bad request. Ensure 'name' & 'price' are included in the JSON payload.")

    if item := items.get(item_id):
        item["price"] = item_data["price"]
        item["name"] = item_data["name"]
        return {"message": "Item updated"}
    abort(404, message="Item not found.")
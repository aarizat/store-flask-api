import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items


blp = Blueprint("Items", __name__, description="Operations on Items")


@blp.route("/items/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        if item := items.get(item_id):
            return item
        abort(404, message="item not found.")

    def delete(self, item_id):
        if items.get(item_id):
            del items[item_id]
            return {"message": "item deleted"}
        abort(404, message="item not found.")

    def put(self, item_id):
        item_data = request.get_json()
        if "name" not in item_data or "price" not in item_data:
            abort(400, message="Bad request. Ensure 'name' & 'price' are included in the JSON payload.")

        if item := items.get(item_id):
            item["price"] = item_data["price"]
            item["name"] = item_data["name"]
            return {"message": "Item updated"}
        abort(404, message="Item not found.")


@blp.route("/items")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if "name" not in item_data:
            abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")

        for item in items.values():
            if item.get("name") == item_data.get("name"):
                abort(400, message="item already exist.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201
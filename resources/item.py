import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on Items")


@blp.route("/items/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        if item := items.get(item_id):
            return item
        abort(404, message="item not found.")

    def delete(self, item_id):
        if items.get(item_id):
            del items[item_id]
            return {"message": "item deleted"}
        abort(404, message="item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        if item := items.get(item_id):
            item["price"] = item_data["price"]
            item["name"] = item_data["name"]
            return item
        abort(404, message="Item not found.")


@blp.route("/items")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if item.get("name") == item_data.get("name"):
                abort(400, message="item already exist.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201

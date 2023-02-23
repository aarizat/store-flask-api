import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations on Stores")


@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        if store := stores.get(store_id):
            return store
        abort(404, message="Store not found.")

    def delete(self, store_id):
        if stores.get(store_id):
            del stores[store_id]
            return {"message": "Store deleted"}
        abort(404, message="Store not found.")


@blp.route("/stores")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    @blp.arguments(StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store.get("name") == store_data.get("name"):
                abort(400, message="Store already exist.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201

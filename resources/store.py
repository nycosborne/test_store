import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("store", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            return {"message": "Store not found"}, 400

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store was deleted"}, 204
        except KeyError:
            return {"message": "Store not found"}, 400


@blp.route("/stores")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        request_data = request.get_json()
        if "name" not in request_data:
            abort(400, description="Missing store name in payload")

        for store in stores.values():
            if request_data["name"] == store["name"]:
                abort(400, description="Store with this name already exists")

        store_id = uuid.uuid4().hex
        store_new = {**request_data, "store_id": store_id}
        stores[store_id] = store_new
        return store_new, 201

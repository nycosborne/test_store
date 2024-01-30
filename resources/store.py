import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("store", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class StoreList(MethodView):
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

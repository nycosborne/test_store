import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemas import StoreSchema

blp = Blueprint("Stores", "stores", description="Operations on stores")


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


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, request_data):
        store = StoreModel(**request_data)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="oter" + str(e))

        return store

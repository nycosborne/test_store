from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import StoreSchema

blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(201, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store1 = StoreModel.query.get_or_404(store_id)
        db.session.delete(store1)
        db.session.commit()

        return {"Message": "Deleted Store Id: " + store_id}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, request_data):
        store = StoreModel(**request_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError as e:
            abort(500, message="Looking like this store name has been taken" + str(e))
        except SQLAlchemyError as e:
            abort(500, message="oter" + str(e))

        return store

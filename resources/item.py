import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemsSchema, ItemUpdate

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):  # Get item by Id
    @blp.response(200, ItemsSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return {"message": "Item not found"}, 400

    def delete(self, item_id):  # delete item by Id
        try:
            del items[item_id]
            return {"message": "Item was deleted"}, 204
        except KeyError:
            abort(404, description="Unable to find item")

    @blp.arguments(ItemUpdate)
    def put(self, item_data, item_id):  # Update item by id
        try:
            print(item_data)
            item = items[item_id]
            item |= item_data
            return {"message": (item_data, {"item ID:": item_id, "New Item": item})}, 201
        except KeyError:
            abort(404, description="Item not found.")


@blp.route("/items")
class ItemList(MethodView):
    def get(self):  # Get all stores
        return {"stores": list(items.values())}

    @blp.arguments(ItemsSchema)
    def post(self, item_data):  # Added new item
        for item in items.values():
            if (
                    item_data["name"] == item["name"]
                    and item_data["store_id"] == item["store_id"]
            ):
                abort(400, description="Already have item")

        if item_data["store_id"] not in stores:
            # return {"message": item_data}, 404
            abort(404, description="Item not found.")

        item_id = uuid.uuid4().hex
        item_new = {**item_data, "id": item_id}
        items[item_id] = item_new

        return {"message": (item_data, {"item ID:": item_id})}, 201

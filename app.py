import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores
from resources import store

from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)

# @app.get('/stores')  # BASE/stores
# def get_stores():  # put application's code here
#     return {"stores": list(stores.values())}
#
#
# @app.get('/items')  # BASE/stores
# def get_items():  # put application's code here
#     return {"items": list(items.values())}
#
#
# @app.get("/store/<string:store_id>")  # BASE/stores
# def get_store_by_id(store_id):  # put application's code here
#     try:
#         return stores[store_id]
#     except KeyError:
#         return {"message": "Store not found"}, 400
#
#
# @app.delete("/store/<string:store_id>")  # BASE/stores
# def delete_store_by_id(store_id):  # put application's code here
#     try:
#         del stores[store_id]
#         return {"message": "Store was deleted"}, 204
#     except KeyError:
#         return {"message": "Store not found"}, 400
#
#
# @app.get("/item/<string:item_id>")
# def get_item_by_id(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, description="Unable to find item")
#
#
# @app.delete("/item/<string:item_id>")
# def delete_item_by_id(item_id):
#     try:
#         del items[item_id]
#         return {"message": "Item was deleted"}, 204
#     except KeyError:
#         abort(404, description="Unable to find item")
#
#
# @app.post('/store')  # BASE/stores
# def create_store():  # put application's code here
#     request_data = request.get_json()
#     if "name" not in request_data:
#         abort(400, description="Missing store name in payload")
#
#     for store in stores.values():
#         if request_data["name"] == store["name"]:
#             abort(400, description="Store with this name already exists")
#
#     store_id = uuid.uuid4().hex
#     store_new = {**request_data, "store_id": store_id}
#     stores[store_id] = store_new
#     return store_new, 201
#
#
# @app.post("/item")
# def add_item():
#     item_data = request.get_json()
#
#     if ("price" not in item_data
#             or "store_id" not in item_data
#             or "name" not in item_data):
#         abort(400, description="Bad JSON payload")
#
#     for item in items.values():
#         if (
#                 item_data["name"] == item["name"]
#                 and item_data["store_id"] == item["store_id"]
#         ):
#             abort(400, description="Already have item")
#
#     if item_data["store_id"] not in stores:
#         # return {"message": item_data}, 404
#         abort(404, description="Item not found.")
#
#     item_id = uuid.uuid4().hex
#     item_new = {**item_data, "id": item_id}
#     items[item_id] = item_new
#     return {"message": (item_data, {"item ID:": item_id})}, 201
#
#
# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
#         abort(400, description="Bad JSON payload")
#     try:
#         print(item_data)
#         item = items[item_id]
#         item |= item_data
#         return {"message": (item_data, {"item ID:": item_id, "New Item": item})}, 201
#     except KeyError:
#         abort(404, description="Item not found.")


if __name__ == '__main__':
    app.run(debug=True, port=5001)

import uuid
from flask import Flask, request
from db import items, stores

app = Flask(__name__)


@app.get('/stores')  # BASE/stores
def get_stores():  # put application's code here
    return {"stores": list(stores.values())}


@app.get('/items')  # BASE/stores
def get_items():  # put application's code here
    return {"items": list(items.values())}


@app.get("/store/<int:store_id>")  # BASE/stores
def get_store_by_id(store_id):  # put application's code here
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404


@app.post('/store')  # BASE/stores
def create_store():  # put application's code here
    request_data = request.get_json()
    store_id = uuid.uuid4().hex
    store_new = {**request_data, "store_id": store_id}
    stores[store_id] = store_new
    return store_new, 201

@app.post("/item")
def add_item():
    item_data = request.get_json()

    if item_data["store_id"] not in stores:
        return {"message": item_data}, 404

    item_id = uuid.uuid4().hex
    item_new = {**item_data, "id": item_id}
    items[item_id] = item_new
    return {"message": item_data}



if __name__ == '__main__':
    app.run(debug=True, port=5001)

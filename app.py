import uuid
from flask import Flask, request
from db import items, stores

app = Flask(__name__)

@app.get('/stores')  # BASE/stores
def get_stores():  # put application's code here
    return {"stores": list(stores.values())}


@app.get("/store/<int:store_id>")  # BASE/stores
def get_one_stores(store_id):  # put application's code here
    return stores[store_id]


@app.post('/store')  # BASE/stores
def create_store():  # put application's code here
    request_data = request.get_json()
    store_id = uuid.uuid4().hex
    # new_store = {"name": request_data["name"], "items": []}
    store = {**request_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/store/<string:name>/item")
def add_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return stores, 201

    return {"message": "Store Not Found"}, 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)

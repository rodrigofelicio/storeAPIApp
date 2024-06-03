import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores


app = Flask(__name__)


########### STORE(S) CRUD ###########
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}, 201


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        # Here you might also want to add the items in this store
        # We'll do that later on in the course
        return stores[store_id], 201
    except KeyError:
        abort(404, message="Store not found")


@app.post("/store")
def create_store():
    store_data = request.get_json()
    
    # Check if there is a name for the store to be added (name must be provided)
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
    # Check if store already exists in the list (name must be unique)
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")
            
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return store, 201


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return { "message": "Store deleted."}, 201
    except KeyError:
        abort(404, message="Store not found.")


########### ITEM(S) CRUD ###########
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}, 201


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 201
    except KeyError:
        abort(404, message="Item not found")
        

@app.post("/item")
def create_item():
    item_data = request.get_json()
    # Here not only we need to validate data exists,
    # But also what type of data. Price should be a float,
    # for example.
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
        )    
    # Validate if the same item exists in the list of items so it can not be added twice
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(
                400,
                message=f"Item already exists."
            )    
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if 'price' not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price', and 'name'are included in the JSON payload.")    
    try:
        item = items[item_id]        
        item |= item_data # this is the new dictionary update operator ( "|=" )                
        
        return item, 201
    except KeyError:
        abort(404, message="Item not found.")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return { "message": "Item deleted."}, 201
    except KeyError:
        abort(404, message="Item not found.")
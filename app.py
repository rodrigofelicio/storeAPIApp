##### NEEDED PREVIOUSLY -----   import uuid
##### NEEDED PREVIOUSLY -----   from flask import Flask, request
##### NEEDED PREVIOUSLY -----   from flask_smorest import abort
##### NEEDED PREVIOUSLY -----   from db import items, stores


from flask import Flask
# it connects the flask_smorest extension to the Flask app
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint


app = Flask(__name__)

# If some exception occurs in a flask module, this must be propagated to the main app so that we can see it
app.config["PROPAGATE_EXCEPTIONS"] = True   

# Flask Smorest configurations for API document
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
# The config below tells Flask Smores what is the root of the API
app.config["OPENAPI_URL_PREFIX"] = "/"

# The configuration below tells flask_smorest to use swagger to document the app
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)







#######
####### THE CODE BELOW IS NOT NEEDED ONCE WE ARE USING BLUEPRINTS AND METHODVIEWS
#######
##############
##############






############ STORE(S) CRUD ###########
#@app.get("/store")
#def get_stores():
#    return {"stores": list(stores.values())}, 201
#
#
#@app.get("/store/<string:store_id>")
#def get_store(store_id):
#    try:
#        # Here you might also want to add the items in this store
#        # We'll do that later on in the course
#        return stores[store_id], 201
#    except KeyError:
#        abort(404, message="Store not found")
#
#
#@app.post("/store")
#def create_store():
#    store_data = request.get_json()
#    
#    # Check if there is a name for the store to be added (name must be provided)
#    if "name" not in store_data:
#        abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
#    # Check if store already exists in the list (name must be unique)
#    for store in stores.values():
#        if store_data["name"] == store["name"]:
#            abort(400, message=f"Store already exists.")
#            
#    store_id = uuid.uuid4().hex
#    store = {**store_data, "id": store_id}
#    stores[store_id] = store
#
#    return store, 201
#
#
#@app.delete("/store/<string:store_id>")
#def delete_store(store_id):
#    try:
#        del stores[store_id]
#        return { "message": "Store deleted."}, 201
#    except KeyError:
#        abort(404, message="Store not found.")
#
#
############ ITEM(S) CRUD ###########
#@app.get("/item")
#def get_all_items():
#    return {"items": list(items.values())}, 201
#
#
#@app.get("/item/<string:item_id>")
#def get_item(item_id):
#    try:
#        return items[item_id], 201
#    except KeyError:
#        abort(404, message="Item not found")
#        
#
#@app.post("/item")
#def create_item():
#    item_data = request.get_json()
#    # Here not only we need to validate data exists,
#    # But also what type of data. Price should be a float,
#    # for example.
#    if (
#        "price" not in item_data
#        or "store_id" not in item_data
#        or "name" not in item_data
#    ):
#        abort(
#            400,
#            message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
#        )
#    for item in items.values():
#        if (
#            item_data["name"] == item["name"]
#            and item_data["store_id"] == item["store_id"]
#        ):
#            abort(400, message=f"Item already exists.")
#
#    item_id = uuid.uuid4().hex
#    item = {**item_data, "id": item_id}
#    items[item_id] = item
#
#    return item
#
#
#@app.put("/item/<string:item_id>")
#def update_item(item_id):
#    item_data = request.get_json()
#    if 'price' not in item_data or "name" not in item_data:
#        abort(400, message="Bad request. Ensure 'price', and 'name'are included in the JSON payload.")    
#    try:
#        item = items[item_id]        
#        item |= item_data # this is the new dictionary update operator ( "|=" )                
#        
#        return item, 201
#    except KeyError:
#        abort(404, message="Item not found.")
#
#
#@app.delete("/item/<string:item_id>")
#def delete_item(item_id):
#    try:
#        del items[item_id]
#        return { "message": "Item deleted."}, 201
#    except KeyError:
#        abort(404, message="Item not found.")
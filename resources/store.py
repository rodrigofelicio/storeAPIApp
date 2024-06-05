import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores


blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}, 201
    

    def post(self):
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


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            # Here you might also want to add the items in this store
            # We'll do that later on in the course
            return stores[store_id], 201
        except KeyError:
            abort(404, message="Store not found")

    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return { "message": "Store deleted."}, 201
        except KeyError:
            abort(404, message="Store not found.")
    


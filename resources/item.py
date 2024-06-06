import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items.")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()        
    
    
    #this blp.arguments annotation below adds documentation to the Swagger-UI regarding fields type and validation
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):  # this 2nd parameter (item_data) is going to contain JSON, which is the 
                                # validated fields that the schema requested. It MUST BE ADDED. The JSON that the client sends
                                # is passed through the ItemSchema, it checks that the fields are there and 
                                # they are the valid types and so forth, and then it gives the method, an argument,
                                # which is that validated dictionary.
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item, 201
    
    

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id], 201
        except KeyError:
            abort(404, message="Item not found")    
    

    # the decorators order matters, so it is important to put blp.response deeper in the code.
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]        
            item |= item_data # this is the new dictionary update operator ( "|=" )                
            
            return item, 201
        except KeyError:
            abort(404, message="Item not found.")

        
    def delete(self, item_id):
        try:
            del items[item_id]
            return { "message": "Item deleted."}, 201
        except KeyError:
            abort(404, message="Item not found.")
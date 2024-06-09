from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
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
                                
                                
        item = ItemModel(**item_data)   # we will pass in the data that we receive in the post method with two asterisks and 
                                        # it's going to turn the dictionary into keyword arguments so any received data from the client 
                                        # will be turned into key arguments and we're going to pass it to ItemModel and when we create an ItemModel class
                                        # all of the ItemModel values, the columns, can be passed as keyword 
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
    
    

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
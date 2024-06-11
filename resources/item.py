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
        item = ItemModel.query.get_or_404(item_id)  # This query attribute cmoes from flask-sqlalchemy pkg.
                                                    # It does everything for us. It retrieves the item from the 
                                                    # database using the items primary key, and if there is no item
                                                    # with this primary key in the db, then it will automatically abort
                                                    # with a 404 status code, which means Not Found.                                                    
        return item
    

    # the decorators order matters, so it is important to put blp.response deeper in the code.
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not implemented yet.")
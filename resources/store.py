from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
    

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)    
    def post(self, store_data):
        store = StoreModel(**store_data)
        
        try:
            db.session.add(store)
            db.session.commit()            
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store.")
        
        return store


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema(many=True))
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
    


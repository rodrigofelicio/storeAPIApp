from db import db

class ItemModel(db.Model):  # This is a mapping between a row in a table to a Python class, and therefore Python objects
    __tablename__ = "items" # This tells SQLAlchemy we want to create, or use a table called items for this class and all the objects of this class

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    
    store = db.relationship("StoreModel", back_populates="items")
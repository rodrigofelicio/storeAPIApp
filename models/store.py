from db import db

class StoreModel(db.Model):  # This is a mapping between a row in a table to a Python class, and therefore Python objects
    __tablename__ = "stores" # This tells SQLAlchemy we want to create, or use a table callde items for this class and all the objects of this class

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
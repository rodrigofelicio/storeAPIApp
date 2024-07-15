from db import db


# This is a mapping between a row in a table to a Python class, and therefore Python objects
class ItemModel(db.Model):
    # This tells SQLAlchemy we want to create, or use a table called items for this class and all the objects of this class
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    description = db.Column(db.String)

    store_id = db.Column(db.Integer, db.ForeignKey(
        "stores.id"), unique=False, nullable=False)

    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship(
        "TagModel", back_populates="items", secondary="items_tags")

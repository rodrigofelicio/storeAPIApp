
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema


blp = Blueprint("Tags", "tags", description="Operations on tags.")

@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        
        return store.tags.all()  # lazy="dynamic" means 'tags' is a query
    
    
    #this blp.arguments annotation below adds documentation to the Swagger-UI regarding fields type and validation    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id): 
        if TagModel.query.filter(TagModel.store_id == tag_data["store_id"], TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that store.")


        # The original line below was like 'tag = TagModel(**tag_data, store_id=store_id)'
        # Nonetheless, I got an error:   TypeError: models.tag.TagModel() got multiple values for keyword argument 'store_id'
        # Then, I found it in stackoverflow about positional arguments (**tag_data) vs keyword arguments (store_id = store_id)
        # https://stackoverflow.com/questions/21764770/typeerror-got-multiple-values-for-argument
        # After understanding and analysing the answer, I came up with the solution below.
        tag = TagModel(name=tag_data["name"], store_id=tag_data["store_id"])
        
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, str(e))
        
        return tag
    

@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        if item.store.id != tag.store.id:
            abort(400, message="Make sure item and tag belong to the same store before linking.")
        
        item.tags.append(tag) #it treats the tags as a list (flask-sqlalchemy)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")
            
        return tag
    
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")
            

        return {"message": "Item removed from tag", "item": item, "tag": tag}
    

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    
    
    @blp.response(202, description="Deletes a tag if no item is tagged with it.", example={"message": "Tag deleted."})
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(400, description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(400, message="Could not delete tag. Make sure tag is not associated with any items, then try again.")
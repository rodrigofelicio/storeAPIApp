# The schema.py contains the marshmallow structure to validate the request and response messages passed to/by each API endpoint/HTTP method
from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True) #dump_only=True is used when the field must be part of the response message
    name = fields.Str(required=True) #required=True is used when the field must be part of the request message
    price = fields.Float(required=True) #required=True is used when the field must be part of the request message
    

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True) #dump_only=True is used when the field must be part of the response message. Used to send data back to the client
    name = fields.Str(required=True) #required=True is used when the field must be part of the request message


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True) #dump_only=True is used when the field must be part of the response message. Used to send data back to the client
    name = fields.Str() #required=True is used when the field must be part of the request message    


class ItemUpdateSchema(PlainItemSchema):
    name = fields.Str() #optional field. That's why there is no parameter in parenthesis
    price = fields.Float() #optional field. That's why there is no parameter in parenthesis
    store_id = fields.Int() #optional field. That's why there is no parameter in parenthesis


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True) #load_only=True this enable us to pass in the store_id when receiving data from the client
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()))
    tags = fields.List(fields.Nested(PlainTagSchema()))


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
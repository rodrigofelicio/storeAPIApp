# The schema.py contains the marshmallow structure to validate the request and response messages passed to/by each API endpoint/HTTP method
from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    # dump_only=True is used when the field must be part of the response message
    id = fields.Int(dump_only=True)
    # required=True is used when the field must be part of the request message
    name = fields.Str(required=True)
    # required=True is used when the field must be part of the request message
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    # dump_only=True is used when the field must be part of the response message. Used to send data back to the client
    id = fields.Int(dump_only=True)
    # required=True is used when the field must be part of the request message
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    # dump_only=True is used when the field must be part of the response message. Used to send data back to the client
    id = fields.Int(dump_only=True)
    # required=True is used when the field must be part of the request message
    name = fields.Str()


class ItemUpdateSchema(PlainItemSchema):
    name = fields.Str()  # optional field. That's why there is no parameter in parenthesis
    price = fields.Float()  # optional field. That's why there is no parameter in parenthesis
    # optional field. That's why there is no parameter in parenthesis
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):
    # load_only=True this enable us to pass in the store_id when receiving data from the client
    store_id = fields.Int(required=True, load_only=True)

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


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    # load_only=True is important so the password is never returned
    password = fields.Str(required=True, load_only=True)

# The schema.py contains the marshmallow structure to validate the request and response messages passed to/by each API endpoint/HTTP method


from marshmallow import Schema, fields


####### ITEM SCHEMAS #######
class ItemSchema(Schema):
    id = fields.Str(dump_only=True) #dump_only=True is used when the field must be part of the response message
    name = fields.Str(required=True) #required=True is used when the field must be part of the request message
    price = fields.Float(required=True) #required=True is used when the field must be part of the request message
    store_id = fields.Str(required=True) #required=True is used when the field must be part of the request message
    

class ItemUpdateSchema(Schema):
    name = fields.Str() #optional field. That's why there is no parameter in parenthesis
    price = fields.Float() #optional field. That's why there is no parameter in parenthesis




####### STORE SCHEMAS #######
class StoreSchema(Schema):
    id = fields.Str(dump_only=True) #dump_only=True is used when the field must be part of the response message. Used to send data back to the client
    name = fields.Str(required=True) #required=True is used when the field must be part of the request message
    

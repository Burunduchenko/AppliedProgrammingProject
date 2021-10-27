from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class UserSchema(Schema):
    name = fields.String(required=True, validate=Length(min=3))
    surname = fields.String(required=True, validate=Length(min=3))
    username = fields.String(required=True, validate=Length(min=3))
    password = fields.String(required=True, validate=Length(min=6))


class AudienceSchema(Schema):
    number = fields.Integer(strict=True, required=True)
    amount_of_places = fields.Integer(strict=True, required=True)
    status = fields.Integer(strict=True, required=True, validate=Range(min=0, max=1))


class ReservatiobSchema(Schema):
    user_id = fields.Integer(strict=True)
    audience_id = fields.Integer(strict=True, required=True)
    title = fields.String(required=True)
    from_date = fields.DateTime(required=True)
    to_date = fields.DateTime(required=True)


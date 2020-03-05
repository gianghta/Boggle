from marshmallow import Schema, fields, post_dump

from boggle.exceptions import InvalidUsage


class BoardRead(Schema):
    id = fields.Integer()


class BoardWrite(Schema):
    random = fields.Boolean(required=True)
    board = fields.Str()
    duration = fields.Integer(required=True)


class BoardOut(Schema):
    id = fields.Integer()
    token = fields.Str()
    board = fields.Str()
    points = fields.Integer()
    duration = fields.Integer()
    time_left = fields.Integer()

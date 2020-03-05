import secrets
from time import time

from sqlalchemy import and_

from boggle import db
from boggle.utils.db import in_transaction


# Default functions
def unix_time():
    """Return the current unix timestamp."""
    return int(time())


# Generate random token
def generate_token():
    return secrets.token_hex(16)


class BaseModel(db.Model):
    @classmethod
    async def get(cls, as_row_obj=False, **kwargs):
        obj = await cls.query.where(
            and_(getattr(cls, column) == val for column, val in kwargs.items())
        ).gino.first()
        if not obj:
            return None
        return obj if as_row_obj else obj.to_dict()

    @classmethod
    @in_transaction
    async def add(cls, **kwargs):
        created_obj = await cls(**kwargs).create()
        return created_obj.to_dict()

    @classmethod
    @in_transaction
    async def modify(cls, get_kwargs, modify_kwargs):
        row = await cls.get(**get_kwargs, as_row_obj=True)
        await row.update(**modify_kwargs).apply()
        return row.to_dict()


class Board(BaseModel):
    __tablename__ = "board"

    # Columns
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    token = db.Column(db.String(length=32), nullable=False, default=generate_token)
    board = db.Column(db.String(length=255), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    duration = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.BigInteger, nullable=False, default=unix_time)

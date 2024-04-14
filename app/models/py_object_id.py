from bson import ObjectId
from pydantic import BaseModel
from typing import  Any


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_object_id

    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")


    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

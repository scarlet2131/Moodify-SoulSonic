from pydantic import BaseModel, Field as PydanticField, EmailStr
from bson import ObjectId

from app.models.py_object_id import PyObjectId


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    security_question: str
    security_answer: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    id: PyObjectId = PydanticField(default_factory=PyObjectId, alias="_id")

    username: str
    email: EmailStr
    password: str
    security_question: str
    security_answer: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# Define the request model
class SecurityAnswerVerificationRequest(BaseModel):
    username: str
    answer: str
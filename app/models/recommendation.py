from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from app.models.py_object_id import PyObjectId

class RecommendationBase(BaseModel):
    emotion: str
    recommendations: List[str]
class RecommendationCreate(RecommendationBase):
    pass
class RecommendationInDB(RecommendationBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

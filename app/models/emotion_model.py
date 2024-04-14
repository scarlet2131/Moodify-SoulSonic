from datetime import datetime

from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class EmotionResponse(BaseModel):
    question: str
    response: str

class UserEmotionInput(BaseModel):
    responses: List[EmotionResponse]

class TrackRecommendation(BaseModel):
    name: str
    artist: str
    spotify_url: str
    image_url: Optional[str] = None

class EmotionAnalysisResult(BaseModel):
    emotion: str
    recommendations: List[TrackRecommendation]
    timestamp: datetime = None


from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional

class TrackRecommendation(BaseModel):
    name: str
    artist: str
    spotify_url: str
    image_url: Optional[str] = None

class MusicHistory(BaseModel):
    username: str
    emotion: str
    timestamp: datetime
    recommendations: List[TrackRecommendation]

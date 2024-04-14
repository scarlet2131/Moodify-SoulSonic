from datetime import datetime
from typing import List

from pymongo.errors import PyMongoError

from app.db.mongodb_utils import get_database
from app.models.emotion_model import EmotionAnalysisResult


def save_music_history(username: str, analysis_result: EmotionAnalysisResult):
    try:
        db = get_database()
        print('Database connection established.')

        # Prepare the history record
        history_record = {
            "username": username,
            "emotion": analysis_result.emotion,
            "recommendations": [{
                "name": rec.name,
                "artist": rec.artist,
                "spotify_url": rec.spotify_url,
                "image_url": rec.image_url
            } for rec in analysis_result.recommendations],
            "timestamp": analysis_result.timestamp

        }

        # Printing the history record for debugging
        print('History record prepared:', history_record)

        # Insert the record into the database
        result = db.music_history.insert_one(history_record)
        print(f'Record inserted with _id: {result.inserted_id}')

    except PyMongoError as e:
        print('Error saving music history to the database:', e)

def fetch_user_music_history(username: str) -> List[EmotionAnalysisResult]:
    db = get_database()
    history_records = db.music_history.find({"username": username})
    return list(history_records)

def delete_user_music_history(username : str):
    db = get_database()
    result = db.music_history.delete_many({"username": username})
    return result
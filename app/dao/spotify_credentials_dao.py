from pymongo import MongoClient

# spotify_credentials_dao.py

from app.db.mongodb_utils import get_database

def get_spotify_credentials():
    db = get_database()
    credentials_doc = db.spotify_credentials.find_one({})
    if not credentials_doc:
        raise Exception("Spotify credentials not found in the database.")
    return credentials_doc["client_id"], credentials_doc["client_secret"], credentials_doc["scope"]

def get_openai_credentials():
    db = get_database()
    credentials_doc = db.openai_credentials.find_one({})
    if not credentials_doc:
        raise Exception("OpenAI credentials not found in the database.")
    return credentials_doc["api_key"]
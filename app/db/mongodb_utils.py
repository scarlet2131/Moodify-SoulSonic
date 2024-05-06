from pymongo import MongoClient


MONGO_URL="mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
MONGO_DB="music_recommendation_system"

def get_database():
    return client[MONGO_DB]






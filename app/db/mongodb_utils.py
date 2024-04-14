from pymongo import MongoClient


# MONGO_URL="mongodb://localhost:27017"
MONGO_URL = "mongodb://monisha:monisha@ac-ph1g6of-shard-00-00.vbumv5h.mongodb.net:27017,ac-ph1g6of-shard-00-01.vbumv5h.mongodb.net:27017,ac-ph1g6of-shard-00-02.vbumv5h.mongodb.net:27017/?replicaSet=atlas-sfap10-shard-0&ssl=true&authSource=admin"
client = MongoClient(MONGO_URL)
MONGO_DB="music_recommendation_system"

def get_database():
    return client[MONGO_DB]






from app.db.mongodb_utils import get_database
from app.models.user import UserInDB

db = get_database()
def create_user_in_db(user_data: dict):
    user = db["users"].insert_one(user_data)
    return user

def get_user_by_username(username: str):
    user = db["users"].find_one({"username": username})
    if user:
        return UserInDB(**user)
    return None

def get_user_by_email(email: str):
    user = db["users"].find_one({"email": email})
    if user:
        return UserInDB(**user)
    return None

def update_password(username: str, new_password: str):
    return db["users"].update_one({"username": username}, {"$set": {"password": new_password}})
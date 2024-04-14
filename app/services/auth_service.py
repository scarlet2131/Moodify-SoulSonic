from fastapi import HTTPException
from starlette import status

from app.dao.user_dao import create_user_in_db, get_user_by_username, get_user_by_email, update_password
from app.models.user import UserCreate, UserLogin
from app.utils.security import verify_password, get_password_hash



def create_user(user: UserCreate):
    # Check if the username already exists
    existing_user =  get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered.")


    # Check if the email already exists only if the username is unique
    existing_email =  get_user_by_email(user.email)
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    # Hash the password and security answer
    hashed_password = get_password_hash(user.password)
    hashed_security_answer = get_password_hash(user.security_answer)

    # Remove the plain password and security answer from the user object
    user.password = hashed_password
    user.security_answer = hashed_security_answer

    # Create the user in the database
    create_user_in_db(user.dict())

    return {"message": "User created successfully."}

    # Hash the password and security answer

def authenticate_user(user1: UserLogin):
    user =  get_user_by_username(user1.username)
    if not user or not verify_password(user1.password, user.password):
        print(f"Hashed password here : {user.password}")
        return False
    return True

def authenticate_user_by_email(email: str):
    user = get_user_by_email(email)
    if not user:
        return {"status": "new"}
    return {"status": "exists"}

def fetch_security_question(username: str):
    user = get_user_by_username(username)
    if user:
        return user.security_question  # Accessing attribute directly
    return None
def verify_security_answer(username: str, answer: str) -> bool:
    # Fetch user from the database
    user = get_user_by_username(username)
    if not user:
        return False
    # Check if the provided answer matches the stored security answer
    return verify_password(answer,user.security_answer)

def reset_user_password(username: str, new_password: str):
    # Hash the password and security answer
    hashed_password = get_password_hash(new_password)

    return update_password(username, hashed_password)
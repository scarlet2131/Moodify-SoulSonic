from passlib.context import CryptContext
from sqlalchemy import null

# Create a CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def get_password_hash(password):
    return pwd_context.hash(password)

# Function to verify a password against a hash
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

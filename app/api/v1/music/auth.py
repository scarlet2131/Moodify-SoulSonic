import os

from fastapi import APIRouter, Depends, HTTPException, Form, Response, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from itsdangerous import URLSafeTimedSerializer
from starlette.status import HTTP_401_UNAUTHORIZED

from app.models.email_check import EmailCheck
from app.models.user import UserCreate, UserLogin, SecurityAnswerVerificationRequest
from app.services import auth_service

SCOPES = "user-read-private user-read-email"
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT_URL")


# Secret key for cookie
SECRET_KEY = "MonishaWebsitekey"
serializer = URLSafeTimedSerializer(SECRET_KEY)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


router = APIRouter()

# ----------------------- Spotify login ---------------------------
@router.get("/login")
async def login():
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={SCOPES}&redirect_uri={SPOTIFY_REDIRECT_URL}"
    return RedirectResponse(auth_url)

# ----------------------- User Register ---------------------------
@router.post("/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    security_question: str = Form(...),
    security_answer: str = Form(...), response: Response =None
):
    user_dto = UserCreate(
        username=username,
        email=email,
        password=password,
        security_question=security_question,
        security_answer=security_answer
    )
    created_user = auth_service.create_user(user_dto)
    if not created_user:
        raise HTTPException(status_code=400, detail="Error registering user.")

    # Create a session token only after the user is successfully created
    session_token = serializer.dumps({"username": username})

    # Set the session cookie correctly
    response.set_cookie(key="session_token", value=session_token, httponly=True)
    return {"message": "User created successfully."}

# --------------------------------------- Landing page ---------------------------------
@router.post("/checkemail")
def check_email(email_check: EmailCheck):
    return auth_service.authenticate_user_by_email(email_check.email)

# ------------------------------------- User Login ------------------------------------
@router.post("/loginUser")
def login(username: str = Form(...), password: str = Form(...), response: Response = None):
    user_dto = UserLogin(username=username, password=password)
    user = auth_service.authenticate_user(user_dto)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    # Create a session token
    session_token = serializer.dumps({"username": username})

    # Set the session cookie correctly
    response.set_cookie(key="session_token", value=session_token, httponly=True)

    return {"message": "Login successful."}

@router.get("/protected")
async def protected_endpoint(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Session token not found.",
        )

    try:
        payload = serializer.loads(session_token)
        return {"message": f"Welcome {payload['username']}!"}
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )


@router.post("/token")
def create_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"session_token": form_data.username, "token_type": "bearer"}

# ----------------------------- Logout  -----------------------------------------
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="session_token")
    return {"message": "Logout successful"}

# ----------------------------- Reset password  -----------------------------------------

@router.get("/get-security-question")
async def get_security_question(username: str):
    question = auth_service.fetch_security_question(username)
    if question is None:
        raise HTTPException(status_code=401, detail="Username does not exist")
    return {"security_question": question}

@router.post("/verify-security-answer")
async def verify_security_answer(request: SecurityAnswerVerificationRequest):
    is_correct = auth_service.verify_security_answer(request.username, request.answer)

    if is_correct:
        return {"verified": True}
    else:
        raise HTTPException(status_code=400, detail="Incorrect security answer")

@router.post("/reset-password")
async def reset_password(username: str, new_password: str):

    if auth_service.reset_user_password(username, new_password):
        return {"message": "Password updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update password")


# ----------------------------- Local testing -----------------------------------------
@router.post("/localregister")
def register(user: UserCreate):
    user =  auth_service.create_user(user)
    if not user:
        raise HTTPException(status_code=400, detail="Error registering user.")
    return {"message": "User created successfully."}

@router.post("/localLogin")
def register(user: UserLogin):
    user =  auth_service.authenticate_user(user)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    return {"message": "Login successful."}
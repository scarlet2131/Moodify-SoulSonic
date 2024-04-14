from typing import List

from fastapi import APIRouter, HTTPException, Header, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.v1.music.auth import serializer
from app.models.emotion_model import UserEmotionInput, EmotionAnalysisResult, TrackRecommendation
from app.services import emotion_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = serializer.loads(token)
        username = payload.get('username')
        return {"username": username}
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials"
        )

@router.post("/analyze-emotions", response_model=EmotionAnalysisResult)
async def analyze_emotions(request: Request, user_input: UserEmotionInput):
    # Extract session token from cookies
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    try:
        # Attempt to deserialize the session token to get the payload
        payload = serializer.loads(session_token)
        username = payload.get("username")
        if not username:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # Now that we have the username, proceed with the analysis
        emotion_result_data = await emotion_service.analyze_and_fetch_recommendations(user_input, username=username)
        # Assuming emotion_result_data is a dict with 'emotion' and a list of 'recommendations'
        return emotion_result_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[EmotionAnalysisResult])
async def get_music_history(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Session token not found.")

    try:
        payload = serializer.loads(session_token)
        username = payload.get("username")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid session token.")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    history_data = emotion_service.fetch_user_history(username)
    if not history_data:
        return []
    return history_data

@router.delete("/history")
async def delete_user_history(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Session token not found.")
    try:
        payload = serializer.loads(session_token)
        username = payload.get("username")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid session token.")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    try:
        result = emotion_service.delete_music_history(username)
        return {"status": "success", "deleted_count": result.deleted_count}
    except Exception as e:
        return {"status": "error", "message": str(e)}

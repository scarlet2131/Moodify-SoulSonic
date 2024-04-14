# Create a router for authentication-related operations
import os

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import RedirectResponse

from app.services import spotify_service

load_dotenv()
SCOPES = "user-read-private user-read-email"
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT_URL")

router = APIRouter()

@router.get("/login")
async def login():

    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={SCOPES}&redirect_uri={SPOTIFY_REDIRECT_URL}"
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(code: str):
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URL,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=token_data)
        token_response_json = token_response.json()
        access_token = token_response_json.get("access_token")

        if not access_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spotify authentication failed.")

        return {"access_token": access_token}

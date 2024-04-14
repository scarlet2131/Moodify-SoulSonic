from datetime import datetime
from typing import List

from app.dao.music_dao import save_music_history, fetch_user_music_history, delete_user_music_history
from app.models.emotion_model import UserEmotionInput, EmotionAnalysisResult
from app.utils.llm_emotion_analyzer import analyze_emotion_with_chatgpt
from app.services.spotify_service import fetch_spotify_access_token, fetch_spotify_recommendations


async def analyze_and_fetch_recommendations(user_input: UserEmotionInput, username : str) -> EmotionAnalysisResult:
    concatenated_data = " ".join(
        [f"Question: {response.question} Response: {response.response}" for response in user_input.responses])
    deduced_emotion = analyze_emotion_with_chatgpt(concatenated_data)

    if not deduced_emotion:
        raise ValueError("Failed to analyze emotion")

    access_token = await fetch_spotify_access_token()
    recommendations = await fetch_spotify_recommendations(access_token, deduced_emotion)

    track_details = [
        {
            "name": track['name'],
            "artist": track['artist'],
            "spotify_url": track['spotify_url'],
            "image_url": track['image_url']
        }
        for track in recommendations
    ]


    current_timestamp = datetime.utcnow()  # Get the current timestamp

    # This is the correct call
    save_music_history(username, EmotionAnalysisResult(emotion=deduced_emotion.get("emotion", "Unknown"),
                                                       recommendations=track_details,
                                                       timestamp=current_timestamp ))

    # Assuming deduced_emotion is a dict that contains 'emotion' key
    return EmotionAnalysisResult(emotion=deduced_emotion.get("emotion", "Unknown"), recommendations=track_details)

def fetch_user_history(username: str) -> List[EmotionAnalysisResult]:
    return fetch_user_music_history(username)

def delete_music_history(username: str ):
    return delete_user_music_history(username)

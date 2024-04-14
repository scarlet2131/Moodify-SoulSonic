import base64

import httpx
import requests
from fastapi import HTTPException, status

from app.dao.spotify_credentials_dao import get_spotify_credentials


async def fetch_spotify_access_token():
    client_id, client_secret, _ = get_spotify_credentials()
    token_url = "https://accounts.spotify.com/api/token"

    # Client credentials must be base64 encoded to be attached to the header
    client_creds = f"{client_id}:{client_secret}"
    encoded_creds = base64.b64encode(client_creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_creds}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    token_data = {
        "grant_type": "client_credentials",
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, headers=headers, data=token_data)
        token_response.raise_for_status()  # This will automatically handle HTTP error responses

    token_response_json = token_response.json()
    access_token = token_response_json.get("access_token")

    if not access_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spotify authentication failed.")

    return access_token

def get_spotify_genre_seeds(access_token):
    """Fetch the list of available genre seeds from Spotify."""
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("genres", [])  # Return the list of genre seeds
    else:
        print(f"Error fetching Spotify genre seeds: {response.status_code}")
        return []


async def get_spotify_artist_id(access_token: str, artist_name: str) -> str:

    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1  # We're only interested in the top result
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(search_url, headers=headers, params=params)
        response.raise_for_status()  # Handle HTTP errors

        search_results = response.json()
        artists = search_results.get("artists", {}).get("items", [])

        if artists:
            # Assuming the top search result is the correct artist
            return artists[0]["id"]
        else:
            return None


async def fetch_spotify_recommendations(access_token: str, chatgpt_response: dict):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limit": 10}  # Adjust according to your needs

    # Add checks and use available information as before
    if 'genre' in chatgpt_response and chatgpt_response['genre']:
        params["seed_genres"] = chatgpt_response['genre']
    if 'artist' in chatgpt_response and chatgpt_response['artist']:
        artist_id = await get_spotify_artist_id(access_token, chatgpt_response['artist'])
        if artist_id:
            params["seed_artists"] = artist_id

    url = "https://api.spotify.com/v1/recommendations"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises an exception for 4XX/5XX responses

            tracks_data = response.json()['tracks']
            recommendations = []
            for track in tracks_data:
                track_info = {
                    "name": track['name'],
                    "artist": ", ".join(artist['name'] for artist in track['artists']),  # Joining all artist names
                    "spotify_url": track['external_urls']['spotify'],
                    "image_url": track['album']['images'][0]['url'] if track['album']['images'] else None
                    # Taking the first image
                }

                recommendations.append(track_info)
            return recommendations
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None  # or an empty list, or a custom error message, depending on your needs

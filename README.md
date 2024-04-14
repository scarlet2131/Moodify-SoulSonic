# Moodify: Music Recommendation System

## Introduction
Moodify is a music recommendation system that suggests music tracks based on your current mood and preferences. This application leverages the Spotify API to fetch music recommendations and OpenAI's ChatGPT for natural language understanding.

## Features
- User authentication and registration
- Mood analysis based on user input
- Music recommendations from Spotify
- History of music recommendations based on user's mood
- Secure password management with reset functionality

## Prerequisites
- Python 3.9 or higher
- Pip (Python package installer)
- MongoDB instance (local or cloud-hosted)
- Spotify Developer account for API access
- OpenAI API access for ChatGPT integration

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/your-username/moodify.git
cd moodify
python -m venv venv
source venv/bin/activate  # For Unix or MacOS
venv\Scripts\activate  # For Windows
```
### Step 2: Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # For Unix or MacOS
venv\Scripts\activate  # For Windows
```
### Step 3:  Install required dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
```bash
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=your_mongodb_uri
```

### Usage
```bash
uvicorn app.main:app --reload
```

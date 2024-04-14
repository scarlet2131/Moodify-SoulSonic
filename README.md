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

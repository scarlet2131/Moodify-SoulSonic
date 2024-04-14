import json

from openai import OpenAI

from app.dao.spotify_credentials_dao import get_openai_credentials

# Load OpenAI credentials
openai_api_key = get_openai_credentials()
client = OpenAI(api_key=openai_api_key)

def generate_prompt(text: str) -> str:
    prompt_text = f"""
    Based on this conversation: "{text}", please analyze and provide a JSON-formatted response that includes:
    - The predominant emotion
    - A suggested music genre
    - A recommended artist
    - A specific mood or vibe for music recommendations
    Format the response as follows:
    {{
        "emotion": "the identified emotion",
        "genre": "suggested genre",
        "artist": "recommended artist",
        "mood": "specific mood or vibe"
    }}
    Please ensure each category is accurately filled based on the conversation.
    """
    return prompt_text


def analyze_emotion_with_chatgpt(text: str) -> dict:

    try:
        # Assume generate_prompt(text) correctly generates the detailed prompt as before
        prompt_text = generate_prompt(text)

        # Make the API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "user", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt_text}
            ]
        )

        # Extract the response text
        response_text = response.choices[0].message.content.strip()

        # Parse the JSON string into a Python dictionary
        response_data = json.loads(response_text)

        # Return the parsed dictionary
        return response_data
    except Exception as e:
        print("Error:", e)
        return {}


import google.generativeai as genai
from config import GEMINI_API_KEY
from database import save_chat
import requests
import time

genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(user_id, message, retries=3):
    """Get AI response from Gemini and save chat history with error handling."""
    model = genai.GenerativeModel("gemini-pro")

    for attempt in range(retries):
        try:
            response = model.generate_content(message)

            bot_response = response.text if response else "Sorry, I couldn't understand."
            save_chat(user_id, message, bot_response)
            return bot_response

        except Exception as e:
            print(f"Error in Gemini API call (Attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retrying

    return "Sorry, I'm having trouble connecting to AI services. Please try again later."
    

def analyze_image(file_path):
    """Use Gemini API to analyze image content."""
    response = requests.post(
        "https://api.gemini.com/v1/image-analysis",
        headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
        files={"file": open(file_path, "rb")}
    )
    return response.json().get("description", "No description available.")
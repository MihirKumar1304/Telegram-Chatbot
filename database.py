from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["telegram_bot"]
users_collection = db["users"]
chats_collection = db["chats"]
files_collection = db["files"]

def save_user(user_id, first_name, username, phone_number=None):
    """Save user details to MongoDB."""
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        users_collection.insert_one({
            "user_id": user_id,
            "first_name": first_name,
            "username": username,
            "phone_number": phone_number
        })

def save_chat(user_id, user_message, bot_response):
    """Save chat history to MongoDB."""
    chats_collection.insert_one({
        "user_id": user_id,
        "user_message": user_message,
        "bot_response": bot_response
    })

def save_file(user_id, file_name, description):
    """Save file metadata to MongoDB."""
    files_collection.insert_one({
        "user_id": user_id,
        "file_name": file_name,
        "description": description
    })

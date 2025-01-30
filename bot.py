from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from database import save_user, save_chat, save_file
from gemini import get_gemini_response
from gemini import analyze_image
from web_search import web_search
from config import TELEGRAM_BOT_TOKEN
import datetime
import os

# Handle /start command
async def start(update: Update, context: CallbackContext):
    """Handle /start command, register users, and request phone number."""
    user = update.message.from_user
    chat_id = update.message.chat_id
    save_user(user.id, user.first_name, user.username)

    # Request phone number
    keyboard = [[KeyboardButton("Share Contact", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text("Welcome! Please share your contact.", reply_markup=reply_markup)

# Handle contact info
async def contact_received(update: Update, context: CallbackContext):
    """Handle phone number received from user."""
    user = update.message.from_user
    phone_number = update.message.contact.phone_number
    save_user(user.id, user.first_name, user.username, phone_number)

    await update.message.reply_text(f"Thanks, {user.first_name}! Your contact has been saved.")

# Handle user messages and store chat history
async def handle_message(update: Update, context: CallbackContext):
    """Handle user messages, store chat history with timestamps."""
    user = update.message.from_user
    user_message = update.message.text
    timestamp = datetime.datetime.utcnow()
    
    bot_response = "Echo: " + user_message  # Placeholder response
    
    # Save chat history
    save_chat(user.id, user_message, bot_response, timestamp)
    
    await update.message.reply_text(bot_response)

# Handle text messages (AI Response via Gemini)
async def handle_message(update: Update, context: CallbackContext):
    """Handle user messages and respond using Gemini AI."""
    user_message = update.message.text
    user_id = update.message.from_user.id

    # Get AI response from Gemini
    bot_response = get_gemini_response(user_id, user_message)
    await update.message.reply_text(bot_response)

# Handle file uploads
async def handle_file(update: Update, context: CallbackContext):
    """Handle file uploads, analyze them, and save metadata."""
    user_id = update.message.from_user.id
    document = update.message.document
    file = await document.get_file()

    download_folder = "downloads"
    os.makedirs(download_folder, exist_ok=True)

    file_path = f"downloads/{document.file_id}_{document.file_name}"
    await file.download_to_drive(file_path)

    description = analyze_image(file_path)
    save_file(user_id, file.file_id, description)

    await update.message.reply_text(f"File analyzed: {description}")

# Handle web search command
async def handle_web_search(update: Update, context: CallbackContext):
    """Handle web search command."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a search query.")
        return

    results = web_search(query)
    await update.message.reply_text(results)

# Main function to initialize bot and add handlers
def main():
    """Initialize the bot and add handlers."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Command Handlers
    app.add_handler(CommandHandler("start", start))

    # Message Handlers
    app.add_handler(MessageHandler(filters.CONTACT, contact_received))  
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  

    # File Handlers
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))  
    
    # Web Search Handler
    app.add_handler(CommandHandler("websearch", handle_web_search))  

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

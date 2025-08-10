import os
import cv2
import numpy as np
import threading
from fastapi import FastAPI
from pyrogram import Client, filters
from pyrogram.types import Message

# ======================
# ENVIRONMENT VARIABLES
# ======================
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ======================
# FASTAPI APP (for Render)
# ======================
web_app = FastAPI()

@web_app.get("/")
def home():
    return {"status": "Bot is running on Render!"}

# ======================
# TELEGRAM BOT
# ======================
bot = Client("sketch_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.photo)
async def sketch_handler(_, message: Message):
    # Download image
    file_path = await message.download()
    
    # Read image
    image = cv2.imread(file_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert colors
    inverted = cv2.bitwise_not(gray)

    # Blur image
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)

    # Create pencil sketch
    inverted_blur = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray, inverted_blur, scale=256.0)

    # Save sketch
    output_path = "sketch.png"
    cv2.imwrite(output_path, sketch)

    # Send back to user
    await message.reply_photo(output_path, caption="🖌 Here’s your humanised sketch!")

    # Cleanup
    os.remove(file_path)
    os.remove(output_path)

# ======================
# START BOT IN BACKGROUND
# ======================
def start_bot():
    bot.run()

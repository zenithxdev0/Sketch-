import os
import cv2
import numpy as np
import tempfile
import threading

from pyrogram import Client, filters
from pyrogram.types import Message
from fastapi import FastAPI

# Environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

# Pyrogram client
app_bot = Client(
    "sketch_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# FastAPI app for HTTP ping
web_app = FastAPI()

@web_app.get("/")
def home():
    return {"status": "Bot is running"}

def photo_to_sketch(path: str) -> str:
    """Convert image to pencil sketch and return output file path."""
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray, inverted_blur, scale=256.0)

    output_path = tempfile.mktemp(suffix=".png")
    cv2.imwrite(output_path, sketch)
    return output_path

@app_bot.on_message(filters.photo)
async def handle_photo(client: Client, message: Message):
    await message.reply_chat_action("upload_photo")
    file_path = await message.download()
    sketch_path = photo_to_sketch(file_path)
    await message.reply_photo(sketch_path, caption="🎨 Here’s your humanised sketch!")
    os.remove(file_path)
    os.remove(sketch_path)

@app_bot.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("👋 Send me a photo and I’ll turn it into a human-like pencil sketch!")

def run_bot():
    app_bot.run()

# Start Pyrogram bot in a separate thread
threading.Thread(target=run_bot, daemon=True).start()

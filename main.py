import os
import asyncio
import cv2
from fastapi import FastAPI
from pyrogram import Client, filters
from pyrogram.types import Message

# ==========
# ENV VARS
# ==========
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ==========
# TELEGRAM BOT
# ==========
bot = Client("sketch_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    await message.reply_text(
        "👋 Hey! Send me a photo and I'll turn it into a humanised sketch for you!"
    )

@bot.on_message(filters.photo)
async def sketch_handler(_, message: Message):
    file_path = await message.download()
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray, inverted_blur, scale=256.0)

    output_path = "sketch.png"
    cv2.imwrite(output_path, sketch)

    await message.reply_photo(output_path, caption="🖌 Here’s your humanised sketch!")

    os.remove(file_path)
    os.remove(output_path)

# ==========
# FASTAPI APP
# ==========
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Bot is running on Render!"}

@app.on_event("startup")
async def startup_event():
    await bot.start()

    # Keep bot alive in background without idle()
    async def run_bot():
        while True:
            await asyncio.sleep(60)

    asyncio.create_task(run_bot())

@app.on_event("shutdown")
async def shutdown_event():
    await bot.stop()

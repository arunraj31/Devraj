from pyrogram import Client, filters, types, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from motor.motor_asyncio import AsyncIOMotorClient
import requests
from config import *
from AiChatBot import Chiku
from pyrogram.enums import ChatAction





@Chiku.on_message(filters.text & ~filters.bot & ~filters.private)
async def handlepvt_message(client, message):
    try:
        if (
            message.text.startswith("!")
            or message.text.startswith("/")
            or message.text.startswith("?")
            or message.text.startswith("@")
            or message.text.startswith("#")
            or message.text.startswith("P")
        ):
            return
        else:
            user_id = message.from_user.id
            user_message = message.text
            api_url = f"http://api.brainshop.ai/get?bid=180331&key=1EGyiLpUu4Vv6mwy&uid={user_id}&msg={user_message}"
            response = requests.get(api_url).json()["cnt"]
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await message.reply_text(response)
    except Exception as e:
        # Optionally, log the exception if needed
        print(f"An error occurred: {str(e)}")

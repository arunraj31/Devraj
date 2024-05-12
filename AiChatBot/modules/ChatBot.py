from pyrogram import Client, filters, types, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from motor.motor_asyncio import AsyncIOMotorClient
import requests
from config import *
from AiChatBot import Chiku
from pyrogram.enums import ChatAction





@Chiku.on_message(filters.text & ~filters.bot & ~filters.private)
async def handlepvt_message(client, message):
    if (
            message.text.startswith("Hello")
            or message.text.startswith("Hi")
            or message.text.startswith("Hii")
            or message.text.startswith("Hui")
            or message.text.startswith("Hlo")
            or message.text.startswith("Hloo")
        ):
            await message.reply_text(f"Hello {message.from_user.mention} How Are You ? \ni hope your fine\n\nIm A Artificial Intelligence Chat Robot Made By @ZeroXCoderZ \nMy Name Is Chiku\nTell Me Something About Yourself ")
    else:
        pass
        
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

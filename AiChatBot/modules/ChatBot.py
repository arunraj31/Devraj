from pyrogram import Client, filters, types, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from motor.motor_asyncio import AsyncIOMotorClient
import requests
from config import *
from AiChatBot import murali as app
from pyrogram.enums import ChatAction
from pymongo import MongoClient


mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.chatbotdbb
chatbotdatabase = db.chatbotdbbb


async def is_admin(chat_id: int, user_id: int) -> bool:
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]


@app.on_message(filters.command("chatbot") & filters.group)
async def chatbot_command(_, message: Message):
    if await is_admin(message.chat.id, message.from_user.id):
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Enable", callback_data="enable_chatbot"),
                    InlineKeyboardButton(text="Disable", callback_data="disable_chatbot"),
                ]
            ]
        )
        await message.reply_text("Choose an option:", reply_markup=keyboard)
    else:
        await message.reply_text("You are not an admin in this group.")


@app.on_callback_query(filters.regex(r"^(enable|disable)_chatbot$"))
async def enable_disable_chatbot(_, query: types.CallbackQuery):
    chat_id = query.message.chat.id
    action = query.data
  
    if await is_admin(chat_id, query.from_user.id):
        if action == "enable_chatbot":
            if await chatbotdatabase.find_one({"chat_id": chat_id}):
                await query.answer("Chatbot is already enabled.")
            else:
                await chatbotdatabase.insert_one({"chat_id": chat_id, "admin_id": query.from_user.id})
                await query.answer("Chatbot enabled successfully!")
                await query.message.edit_text(f"Chatbot enabled by {query.from_user.mention()}")
        else:
            chatbot_info = await chatbotdatabase.find_one({"chat_id": chat_id})
            if chatbot_info:
                await chatbotdatabase.delete_one({"chat_id": chat_id})
                await query.answer("Chatbot disabled successfully!")
                await query.message.edit_text("Chatbot disabled.")
            else:
                await query.answer("Chatbot is not enabled for this chat.")
    else:
        # if not adminn 
        await query.answer("You are not an admin in this group.")



@app.on_message(filters.text & ~filters.bot)
async def handle_message(client, message):
    try:
        chat_id = message.chat.id

        # Check if the message is a reply to the bot or if there's no reply
        if (message.reply_to_message and message.reply_to_message.from_user.is_self) or not message.reply_to_message:

            chatbot_info = await chatbotdatabase.find_one({"chat_id": chat_id})
            if chatbot_info:
                user_id = message.from_user.id
                user_message = message.text
                api_url = f"http://api.brainshop.ai/get?bid=180331&key=1EGyiLpUu4Vv6mwy&uid={user_id}&msg={user_message}"
                response = requests.get(api_url).json()["cnt"]
                await client.send_chat_action(message.chat.id, ChatAction.TYPING)
                await message.reply_text(response)
            else:
                pass  # If chatbot is not enabled, do nothing
        else:
            pass  # If the message doesn't meet the conditions, do nothing.
    except Exception as e:
        # Optionally, log the exception if needed
        print(f"An error occurred: {str(e)}")

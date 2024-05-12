from pyrogram import Client, filters, types, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from motor.motor_asyncio import AsyncIOMotorClient
import requests
from config import *
from AiChatBot import murali as app
from pyrogram.enums import ChatAction
from pymongo import MongoClient
import emoji


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



@app.on_message(filters.group)
async def chat_bot(client, message):
    url = "https://adult-gpt.p.rapidapi.com/adultgpt"

    payload = {
        "messages": [
            {
                "role": "user",
                "content": message.text
            }
        ],
        "genere": "ai-hen-rei_suz",
        "bot_name": "",
        "temperature": 0.9,
        "top_k": 10,
        "top_p": 0.9,
        "max_tokens": 200
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "5198e8e03dmsh8964c5e124e2423p1465fcjsn24fee55d765b",
        "X-RapidAPI-Host": "adult-gpt.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    result = response.json().get('result')
    await message.reply_text(result)

# Run the bot
app.run()

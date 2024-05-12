from pyrogram import Client, filters, types, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import requests
from AiChatBot import murali as app
from pyrogram.enums import ChatAction





@app.on_message(filters.private & filters.text)
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
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    await message.reply_text(result)


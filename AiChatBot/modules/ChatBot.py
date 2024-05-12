from pyrogram import Client, filters, types, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from motor.motor_asyncio import AsyncIOMotorClient
import requests
from config import *
from AiChatBot import Chiku
from pyrogram.enums import ChatAction, ChatType

Emojis = [
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇",
    "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚",
    "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩",
    "🥳", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣",
    "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬",
    "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗",
    "🤔", "🤭", "🤫", "🤥", "😶‍🌫️", "😐", "😑", "😬", "🙄", "😯",
    "😦", "😧", "😮‍💨", "😲", "🥱", "😴", "😪", "😌", "🥴", "😵",
    "🤐", "🤢", "🤮", "🤧", "😷", "🤒", "🤕", "🤑", "🤠", "😈",
    "👿", "👹", "👺", "🤡", "💩", "👻", "💀", "☠️", "👽", "👾",
    "🤖", "🎃", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿",
    "😾", "🌋", "👀", "🥀"
]

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.chatbotdbb
chatbotdatabase = db.chatbotdbbb

async def is_admin(chat_id: int, user_id: int) -> bool:
    member = await Chiku.get_chat_member(chat_id, user_id)
    return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]

@Chiku.on_message(filters.command("chatbot") & filters.group)
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

@Chiku.on_callback_query(filters.regex(r"^(enable|disable)_chatbot$"))
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
        await query.answer("You are not an admin in this group.")

@Chiku.on_message(filters.text & ~filters.bot)
async def handle_message(client, message):  
    if message.chat.type == ChatType.PRIVATE:
        for emoji in Emojis:
            if emoji in message.text:
                return
        try:
            if (
                message.text.startswith("Hello")
                or message.text.startswith("Hi")
                or message.text.startswith("Hii")
                or message.text.startswith("Hui")
                or message.text.startswith("Hlo")
                or message.text.startswith("Hloo")
            ):
                await message.reply_text(f"Hello {message.from_user.mention} How Are You ? \ni hope your fine\n\nIm A Artificial Intelligence Chat Robot Made By @ZeroXCoderZ \nMy Name Is Chiku\nTell Me Something About Yourself ")
                return
            else:
                pass
            
            if (
                message.text.startswith("!")
                or message.text.startswith("/")
                or message.text.startswith("?")
                or message.text.startswith("@")
                or message.text.startswith("#")
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
            print(f"An error occurred: {str(e)}")
    else:
        if (message.reply_to_message and message.reply_to_message.from_user.is_self) or not message.reply_to_message:
            chat_id = message.chat.id
            chatbot_info = await chatbotdatabase.find_one({"chat_id": chat_id})
            if chatbot_info:
                for emoji in Emojis:
                    if emoji in message.text:
                        return
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
                    print(f"An error occurred: {str(e)}")
            else:
                pass

from pyrogram import Client, filters, types, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from motor.motor_asyncio import AsyncIOMotorClient
import requests
from config import *
from AiChatBot.Db import add_served_user, add_served_chat, get_served_chats, get_served_users
from AiChatBot import Chiku, LOGGER_ID
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
        response = requests.get("https://nekos.best/api/v2/neko").json()
        image_url = response["results"][0]["url"]
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Eɴᴀʙʟᴇ", callback_data="enable_chatbot"),
                    InlineKeyboardButton(text="Dᴇsᴀʙʟᴇ", callback_data="disable_chatbot"),
                ]
            ]
        )
        await message.reply_photo(image_url, caption="Choose an option:", reply_markup=keyboard)
    else:
        await message.reply_text("You are not an admin in this group.")

@Chiku.on_callback_query(filters.regex(r"^(enable|disable)_chatbot$"))
async def enable_disable_chatbot(_, query: types.CallbackQuery):
    chat_id = query.message.chat.id
    action = query.data
  
    if await is_admin(chat_id, query.from_user.id):
        if action == "enable_chatbot":
            if await chatbotdatabase.find_one({"chat_id": chat_id}):
                await query.answer("Chatbot is already enabled.", show_alert=true)
            else:
                await chatbotdatabase.insert_one({"chat_id": chat_id, "admin_id": query.from_user.id})
                await query.answer("Chatbot enabled successfully!", show_alert=true)
                await query.message.edit_text(f"Chatbot enabled by {query.from_user.mention()}")
        else:
            chatbot_info = await chatbotdatabase.find_one({"chat_id": chat_id})
            if chatbot_info:
                await chatbotdatabase.delete_one({"chat_id": chat_id})
                await query.answer("Chatbot disabled successfully!", show_alert=true)
                await query.message.edit_text("Chatbot disabled.")
            else:
                await query.answer("Chatbot is not enabled for this chat.", show_alert=true)
    else:
        await query.answer("You are not an admin in this group.", show_alert=true)



@Chiku.on_message(filters.text & ~filters.bot)
async def handle_message(client, message):  
    response = requests.get("https://nekos.best/api/v2/neko").json()
    image_url = response["results"][0]["url"]
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    try:
        await Chiku.resolve_peer(OWNER_ID[0])
        OWNER = OWNER_ID[0]
    except:
        OWNER = OWNER_ID[0]
    user_id = message.from_user.id
    if "Developer" in message.text:
        return await message.reply_text("My Developer Is My Cute Owner Murali (@ZeroXCoderz)")
    if "I Hate You" in message.text:
        return await message.reply_text("Please tell me what I did to make you angry? \nYour Feedback Is Important To Me \nPlease Report To My Devoloper")
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
                await message.reply_text(f"Hello {message.from_user.first_name} How Are You ? \ni hope your fine\n\nIm A Artificial Intelligence Chat Robot Made By @ZeroXCoderZ \nMy Name Is Chiku\nTell Me Something About Yourself ")
                return
            else:
                pass
        except Exception:
            pass
        try:
            if (
                message.text.startswith("!")
              #  or message.text.startswith("/")
                or message.text.startswith("?")
                or message.text.startswith("@")
                or message.text.startswith("#")
            ):
                return
        except Exception:
            pass
        if message.text.startswith("/start"):
            await message.reply_photo(image_url, caption=f"ʜᴇʟʟᴏ {message.from_user.first_name}\n\nMʏ Nᴀᴍᴇ Is Cʜɪᴋᴜ 🥀\nᴀ ᴀʀᴛɪғɪᴄɪᴀʟ ɪɴᴛᴇʟʟɪɢᴇɴᴄᴇ ᴄʜᴀᴛ ʙᴏᴛ ❄️\n<u>sᴜᴘᴘᴏʀᴛᴇᴅ ʟᴀɴɢᴜᴀɢᴇs</u>: Eɴɢʟɪsʜ Aɴᴅ Cʜɪɴᴇsᴇ 🎄", reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 💓",
                        url=f"https://t.me/ChikuOpBot?startgroup=true",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="ᴍʏ ᴄᴜᴛᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ 🥀",
                        user_id=OWNER,
                    ),
                ],
            ]
            )
                                     )
            await add_served_user(user_id)
            await Chiku.send_message(LOGGER_ID, f"{message.from_user.mention} Has Just Started Bot \n\nName - {message.from_user.first_name}\nId - {message.from_user.id} ")
        else:
            pass        
        if message.text.startswith("/stats"):
            await message.reply_text(
            f"""ᴛᴏᴛᴀʟ sᴛᴀᴛs ᴏғ chiku bot :

➻ **ᴄʜᴀᴛs :** {chats}
➻ **ᴜsᴇʀs :** {users}
"""
            )
        else:
            pass
            
        try:
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
                        #or message.text.startswith("/")
                        or message.text.startswith("?")
                        or message.text.startswith("@")
                        or message.text.startswith("#")
                    ):
                        return
                except Exception:
                    pass
                if "Developer" in message.text:
                    return await message.reply_text("My Developer Is My Cute Owner Murali (@ZeroXCoderz)")
                if "owner" in message.text:
                    return await message.reply_text("my cute owner is Murali ")
                try:
                    user_id = message.from_user.id
                    user_message = message.text
                    api_url = f"http://api.brainshop.ai/get?bid=180331&key=1EGyiLpUu4Vv6mwy&uid={user_id}&msg={user_message}"
                    response = requests.get(api_url).json()["cnt"]
                    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
                    await message.reply_text(response)
                    try:
                        await add_served_chat(message.chat.id)
                    except:
                        pass
                except Exception as e:
                    print(f"An error occurred: {str(e)}")

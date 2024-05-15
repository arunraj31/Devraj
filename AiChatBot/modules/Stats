from AiChatBot import Chiku
from config import OWNER_ID 
from AiChatBot.Db import get_served_chats, get_served_users
from pyrogram import Client, filters
from pyrogram.types import Message

@Chiku.on_message(filters.command("stats"))
async def stats(cli: Client, message: Message):
    if message.from_user.id == OWNER_ID:
        pass
    else:
        return 
    try:
        users = len(await get_served_users())
        chats = len(await get_served_chats())
        await message.reply_text(
            f"""ᴛᴏᴛᴀʟ sᴛᴀᴛs ᴏғ {Chiku.mention} :

➻ **ᴄʜᴀᴛs :** {chats}
➻ **ᴜsᴇʀs :** {users}
"""
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        await message.reply_text("An error occurred while gathering stats.")

from AiChatBot import Chiku
from config import OWNER_ID 
from AiChatBot.Db import get_served_chats, get_served_users
from pyrogram import Client, filters
from pyrogram.types import Message


@Chiku.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(cli: Client, message: Message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    await message.reply_text(
        f"""ᴛᴏᴛᴀʟ sᴛᴀᴛs ᴏғ {Chiku.mention} :

➻ **ᴄʜᴀᴛs :** {chats}
➻ **ᴜsᴇʀs :** {users}
"""
    )

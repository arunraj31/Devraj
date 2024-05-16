import asyncio
import importlib
from pyrogram import idle
from AiChatBot import Chiku, LOGGER_ID
from AiChatBot.modules import ALL_MODULES

loop = asyncio.get_event_loop()

async def pikachuu():
    for all_module in ALL_MODULES:
        importlib.import_module("AiChatBot.modules." + all_module)
    print("𝐂𝐇𝐈𝐊𝐔 𝐁𝐎𝐓 𝐇𝐀𝐒 𝐁𝐄𝐄𝐍 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 ✨")
    await Chiku.send_message(LOGGER_ID, "ᴄʜᴀᴛʙᴏᴛ ɪs sᴛᴀʀᴛᴇᴅ 🌋 \n\nMʏ Cᴜᴛᴇ Dᴇᴠᴇʟᴏᴘᴇʀ @zeroxcoderz")
    await idle()
    
if __name__ == "__main__":
    loop.run_until_complete(pikachuu())
    

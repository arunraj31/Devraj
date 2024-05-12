import asyncio
import importlib
from pyrogram import idle
from AiChatBot import Chiku
from AiChatBot.modules import ALL_MODULES

 from config import LOGGER_ID

loop = asyncio.get_event_loop()

async def pikachuu():
    for all_module in ALL_MODULES:
        importlib.import_module("AiChatBot.modules." + all_module)
    print("𝖻𝗈𝗍 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅 𝗌𝗍𝖺𝗋𝗍")
    await Chiku.send_message(LOGGER_ID, "chat bot start 🌋")
    await idle()
    
if __name__ == "__main__":
    loop.run_until_complete(pikachuu())
    

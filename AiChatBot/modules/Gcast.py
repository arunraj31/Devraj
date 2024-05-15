from AiChatBot import Chiku
import asyncio
from pyrogram import client, filters
from config import OWNER_ID
from pyrogram.errors import FloodWait
from AiChatBot.Db import get_served_chats, get_served_users

@Chiku.on_cmd(["broadcast", "gcast"])
async def braodcast_message(client, message, _):
    if message.from_user.id not in OWNER_ID:
        return await message.reply_text(
            "» 😁 ʜᴇʜᴇʜᴇ ᴏɴʟʏ ᴍʏ ᴏᴡɴᴇʀ ᴄᴀɴ ʙʀᴏᴀᴅᴄᴀsᴛ"
        )
    global IS_BROADCASTING
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(f"**Usage**/n\broadcast Message or reply " )
        query = message.text.split(None, 1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await message.reply_text("give text to broadcast something")

    IS_BROADCASTING = True

    # Bot broadcast inside chats
    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            if i == -1002113460681:
                continue
            try:
                m = (
                    await Chiku.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await Chiku.send_message(i, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except Exception:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except Exception:
                        continue
                sent += 1
            except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                continue
        try:
            await message.reply_text("broadcasted message in {} chats with {} pins from bot ")
        except:
            pass

            
    if "-user" in message.text:
        susr = 0
        served_users = []
        susers = await get_served_users()
        for user in susers:
            served_users.append(int(user["user_id"]))
        for i in served_users:
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await Chiku.send_message(i, text=query)
                )
                susr += 1
            except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                pass
        try:
            await message.reply_text(_["broad_7"].format(susr))
        except:
            pass


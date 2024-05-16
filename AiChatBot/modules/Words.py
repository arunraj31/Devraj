import asyncio
import datetime
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import ChatPermissions
from config import LOGGER_ID as LOG_GROUP_ID
from AiChatBot import Chiku as app
from profanity import profanity


@app.on_message(filters.text & filters.group, group=11)
async def handle_bad_words(client, message):
    try:
        txt = message.text
        user_id = message.from_user.id
        if not profanity.contains_profanity(txt):
            return
        censored_text = profanity.censor(txt)
        bot = (await app.get_chat_member(message.chat.id, app.id)).privileges
        chat_id = message.chat.id
        admins = []
        async for admin in app.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            admins.append(admin.user)

        for admin in admins:
            if admin.is_bot or admin.is_deleted:
                continue
            censored_text += f"[\u2063](tg://user?id={admin.id})"

        if bot.can_delete_messages and not bot.can_restrict_members:
            await message.delete()
            await message.reply_text(
                f"User {message.from_user.mention} has sent **{censored_text}**. i have deleted the bad word but Please give me permission to restrict members in order to automatically mute users who send bad words for 5 minutes."
            )
        elif bot.can_restrict_members and not bot.can_delete_messages:
            mute_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
            await app.restrict_chat_member(
                chat_id, user_id, ChatPermissions(), until_date=mute_time
            )
            await message.reply_text(
                f"{message.from_user.mention} used a bad word: **{censored_text}**, so they are muted for 5 minutes but i have no permission to delete message so give me delete message permission in order to delete bad word automatically",
            )
        elif bot.can_restrict_members and bot.can_delete_messages:
            await message.delete()
            mute_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
            await app.restrict_chat_member(
                chat_id, user_id, ChatPermissions(), until_date=mute_time
            )
            SH = await app.send_message(
                message.chat.id,
                f"{message.from_user.mention} used a bad word: **{censored_text}**, so they are muted for 5 minutes",
            )
            await asyncio.sleep(300)
            await SH.delete()
        elif not bot.can_restrict_members and not bot.can_delete_messages:
            await message.reply_text(
                f"User {message.from_user.mention} has sent **{censored_text}**. the bad word but Please give me permission to restrict members in order to automatically mute users who send bad words for 5 minutes. and delete message permission to delete bad message automatically"
            )

    except Exception as e:
        print(e)
        await app.send_message(LOG_GROUP_ID, f"Error in profanity module: {e}")

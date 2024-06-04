#Github.com/im-Rudraa332

import os
from .. import Bot
from telethon import events, Button
from pyrogram import filters,Client
async def start_srb(event, st):
    await event.reply(st, 
                      buttons=[
                              [Button.inline("✅ Thumbnail", data="set"),
                               Button.inline("❌ Remove Thumbnail", data="rem")],
                              [Button.url("🕉 Join Channel", url="t.me/bot_channelv1")]])
                              
    
async def vc_menu(event):
    await event.edit("**VIDEO CONVERTOR v1.4**", 
                    buttons=[
                        [Button.inline("info.", data="info"),
                         Button.inline("SOURCE", data="source")],
                        [Button.inline("NOTICE.", data="notice"),
                         Button.inline("Main.", data="help")],
                        [Button.url("DEVELOPER", url="t.me/bot_channelv1")]])

#------------------------------------------------------>
from pyrogram import Client
from pyrogram.types import Message

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message
)
# ------------------------------------> Added log channel
from .configs import Config
from .database import Database
import datetime

BOT_USERNAME = Config.BOT_USERNAME
BOT_TOKEN = Config.BOT_TOKEN
API_ID = Config.API_ID
API_HASH = Config.API_HASH
LOG_CHANNEL = Config.LOG_CHANNEL
BOT_OWNER = Config.BOT_OWNER
db= Database(Config.DATABASE_URL, BOT_USERNAME)

async def foo(bot, cmd):
    chat_id = cmd.from_user.id
    if not await db.is_user_exist(chat_id):
        await db.add_user(chat_id)
        await bot.send_message(
            Config.LOG_CHANNEL,
            f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} \n And His/her username is \n **@{cmd.from_user.username}**\n And Userid is `{cmd.from_user.id}` !!"
        )

    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
                datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("You are Banned.", quote=True)
            return
    await cmd.continue_propagation()


@Bot.on_message(filters.private)
async def _(bot, cmd):
    await foo(bot, cmd)

# ----------------------------------------------------------->brodcast message Added

broadcast_ids = {}
import random
import time
import aiofiles
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import asyncio
import traceback
import string
async def send_msg(user_id, message):
    try:
        await message.forward(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast_(c, m):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await m.reply_text(
        text=f"Broadcast Started! You will be notified with log file when all the users are notified."
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(
        total=total_users,
        current=done,
        failed=failed,
        success=success
    )
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(
                user_id=int(user['id']),
                message=broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(
                        current=done,
                        failed=failed,
                        success=success
                    )
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await m.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    os.remove('broadcast.txt')

 
HOME_TEXT = """
Hi, [{}](tg://user?id={})\n\nThis is **Save restricted bot**.

**I can forward restricted content of any group/channel simply**
Send Me A Link Of Your Channel\nIf You Have Private Channel,Send Me Invite #Link First.

"""

# ------------------------------------------------------->




from .. import bot
@bot.on(events.callbackquery.CallbackQuery(data="set"))
async def sett(event):    
    bot = event.client                    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with bot.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Send me An image for Thumbnail")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("No media found.")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("No image found.")
        await xx.delete()
        t = await event.client.send_message(event.chat_id, 'Trying.')
        path = await event.client.download_media(x.media)
        if os.path.exists(f'{event.sender_id}.jpg'):
            os.remove(f'{event.sender_id}.jpg')
        os.rename(path, f'./{event.sender_id}.jpg')
        await t.edit("Thumbnail Accepted!")
        
@bot.on(events.callbackquery.CallbackQuery(data="rem"))
async def remt(event):  
    bot = event.client            
    await event.edit('Trying...')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await event.edit('Tumbnail Removed!')
    except Exception:
        await event.edit("No thumbnail saved.")                        
  
# @bot.on(events.NewMessage(incoming=True, pattern=f"/start"))
# async def start(event):
#     text = "Hi, Sir\n\nThis is **Save Restricted Bot**\n\nSend Me A Link Of Your Channel\nIf You Have Private Channel,Send Me Invite Link First."
#     await start_srb(event, text)
    
# @bot.on(events.NewMessage(incoming=True, pattern=f"/Start"))
# async def start(event):
#     text = "Hi, Sir\n\nThis is **Save Restricted Bot**\n\nSend Me A Link Of Your Channel\nIf You Have Private Channel,Send Me Invite Link First."
#     await start_srb(event, text)



@Bot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, cmd: Message):
        await cmd.reply_text(
            HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
            disable_web_page_preview=True,reply_markup=InlineKeyboardMarkup(
                [
                    [
                         InlineKeyboardButton("✅ Thumbnail", callback_data="set"),
                         InlineKeyboardButton("❌ Remove Thumbnail", callback_data="rem")
                    ],
                    [
                        InlineKeyboardButton("How To Use", url="https://youtu.be/_mdB1L_0Q28")
                    ],
                     [
                        InlineKeyboardButton("Support Group", url="https://t.me/Joint0T"),
                        InlineKeyboardButton("Bots Channel", url="https://t.me/bot_channelv1")
                     ]
                ]
            )
        )


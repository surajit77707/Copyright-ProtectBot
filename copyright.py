import os
import re
import sys
import time
import datetime
import random 
import asyncio
from pytz import timezone
from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.raw.types import UpdateEditMessage, UpdateEditChannelMessage
import traceback

from apscheduler.schedulers.background import BackgroundScheduler


API_ID = 23967991
API_HASH = "a2c3ccfaff4c2dbbff7d54981828d4f1"
BOT_TOKEN = "7848626329:AAE0XlwVEf91Bp0f3tPGjyh60RvhsiS4-qM"
DEVS = [1883889098, 7921906677]
BOT_USERNAME = "Protectorvbot" # change your bot username without 
OWNER_ID = 7921906677

ALL_GROUPS = []
TOTAL_USERS = []
MEDIA_GROUPS = []
DISABLE_CHATS = []
GROUP_MEDIAS = {}

DELETE_MESSAGE = [
"1 Hour complete, I'm doing my work...",
"Its time to delete all medias!",
"No one can Copyright until I'm alive 😤",
"Hue hue, let's delete media...",
"I'm here to delete medias 🙋", 
"😮‍💨 Finally I delete medias",
"Great work done by me 🥲",
"All media cleared!",
"hue hue medias deleted by me 😮‍💨",
"medias....",
"it's hard to delete all medias 🙄",
]

START_MESSAGE = """
**Hello {}, I'm Anti - CopyRight Bot**

 > **I can save your groups from Copyrights 😉**

 **Work:** I'll Delete all medias of your group in every 1 hour ➰
 
 **Process?:** Simply add me in your group and promote as admin with delete messages right!
"""

BUTTON = [[InlineKeyboardButton("+ Add me in group +", url=f"http://t.me/{BOT_USERNAME}?startgroup=s&admin=delete_messages")]]

bot = Client('bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def add_user(user_id):
   if user_id not in TOTAL_USERS:
      TOTAL_USERS.append(user_id)

@bot.on_message(filters.command(["ping", "speed"]))
async def ping(_, e: Message):
   start = datetime.datetime.now()
   add_user(e.from_user.id)
   rep = await e.reply_text("**Pong !!**")
   end = datetime.datetime.now()
   ms = (end-start).microseconds / 1000
   python_version = platform.python_version()
   uptime = time_formatter((time.time() - start_time) * 1000)
   await rep.edit_text(f"🤖 ᑭOᑎᘜ: `{ms}`ᴍs"
                       f"➪ᑌᑭ TIᗰᗴ: {uptime}\n"
                       f"➪ᗷᗩᑎᑎᗴᖇ ᐯᗴᖇՏIOᑎ: {python_version},"
                       f"➪ՏᑌᑭᑭOᖇT: @UmbrellaUCorp ,"
                      )

@bot.on_message(filters.command(["help", "start"]))
async def start_message(_, message: Message):
   add_user(message.from_user.id)
   await message.reply(START_MESSAGE.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(BUTTON))

@bot.on_message(filters.user(DEVS) & filters.command(["restart", "reboot"]))
async def restart_(_, e: Message):
   await e.reply("**Restarting.....**")
   try:
      await bot.stop()
   except Exception:
      pass
   args = [sys.executable, "copyright.py"]
   os.execl(sys.executable, *args)
   quit()

@bot.on_message(filters.user(OWNER_ID) & filters.command(["stat", "stats"]))
async def status(_, message: Message):
    wait = await message.reply("Fetching.....")
    stats = "**Here is total stats of me!** \n\n"
    stats += f"Total Chats: `{len(ALL_GROUPS)}` \n"
    stats += f"Total users: `{len(TOTAL_USERS)}` \n"
    stats += f"Disabled chats: `{len(DISABLE_CHATS)}` \n"
    stats += f"Total Media active chats: `{len(MEDIA_GROUPS)}` \n\n"
    await wait.edit_text(stats)


# Add this function near the other command functions
@bot.on_message(filters.user(OWNER_ID) & filters.command(["bcast"]))
async def broadcast_message(_, message: Message):
    broadcast_text = ' '.join(message.command[1:])
    if not broadcast_text:
        await message.reply("Please provide a message to broadcast.")
        return
    
    success = 0
    failure = 0
    
    # Broadcast to all users
    for user_id in TOTAL_USERS:
        try:
            await bot.send_message(user_id, broadcast_text)
            success += 1
        except Exception:
            failure += 1

    # Broadcast to all groups
    for group_id in ALL_GROUPS:
        try:
            await bot.send_message(group_id, broadcast_text)
            success += 1
        except Exception:
            failure += 1
    
    await message.reply(f"Broadcast completed: {success} success, {failure} failure.")

  # Remove the enable_disable function completely

@bot.on_message(filters.all & filters.group)
async def watcher(_, message: Message):
    chat = message.chat
    user_id = message.from_user.id
    if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
        if chat.id not in ALL_GROUPS:
            ALL_GROUPS.append(chat.id)
        if chat.id not in MEDIA_GROUPS:
            MEDIA_GROUPS.append(chat.id)
        if (message.video or message.photo or message.animation or message.document):
            check = GROUP_MEDIAS.get(chat.id)
            if check:
                GROUP_MEDIAS[chat.id].append(message.id)
                print(f"Chat: {chat.title}, message ID: {message.id}")
            else:
                GROUP_MEDIAS[chat.id] = [message.id]
                print(f"Chat: {chat.title}, message ID: {message.id}")


# Edit Handlers 
@bot.on_raw_update(group=-1)
async def better(client, update, _, __):
    if isinstance(update, UpdateEditMessage) or isinstance(update, UpdateEditChannelMessage):
        e = update.message
        try:            
            if not getattr(e, 'edit_hide', False):      
                user_id = e.from_id.user_id
                if user_id in DEVS:
                    return

                chat_id = f"-100{e.peer_id.channel_id}"
               
                await client.delete_messages(chat_id=chat_id, message_ids=e.id)               
                
                user = await client.get_users(e.from_id.user_id)
                
                await client.send_message(
                    chat_id=chat_id,
                    text=f"{user.mention} just edited a message, and I deleted it 🐸."
                )
        except Exception as ex:
            print("Error occurred:", traceback.format_exc())
         

def AutoDelete():
    if len(MEDIA_GROUPS) == 0:
       return

    for i in MEDIA_GROUPS:
       if i in DISABLE_CHATS:
         return
       message_list = list(GROUP_MEDIAS.get(i))
       try:
          hue = bot.send_message(i, random.choice(DELETE_MESSAGE))
          bot.delete_messages(i, message_list, revoke=True)
          time.sleep(1)
          hue.delete()
          GROUP_MEDIAS[i].delete()
          gue = bot.send_message(i, text="Deleted All Media's")
       except Exception:
          pass
    MEDIA_GROUPS.remove(i)
    print("clean all medias ✓")
    print("waiting for 1 hour")

scheduler = BackgroundScheduler(timezone=timezone('Asia/Kolkata'))
scheduler.add_job(AutoDelete, "interval", seconds=3600)
scheduler.start()

def starter():
   print('Starting Bot...')
   bot.start()
   print('Bot Started ✓')
   idle()

if __name__ == "__main__":
   starter()

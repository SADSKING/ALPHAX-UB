# <--imports-->
from telethon import events 
from telethon import Button
from alphax.config import Config 
# <--Config-->
MANAGER = Config.MANAGER
BOT_USERNAME = Config.BOT_USERNAME
BOT_NAME = Config.BOT_NAME if Config.BOT_NAME else "αℓρнαχ๏ Assistant Manager!"
# <--notes-->
BAN = """
•× `/ban` - (username/id/reply) : Ban the User
•× `/unban` - (username/id/reply) : UnBan the User.

"""
PIN = """
•× `/pin` - Pin a message in group

"""
SHUTUP = """
•× `/mute` - (username/id/reply) :Mute the User.
•× `/unmute` - (username/id/reply) :Unmute the User

"""
PUR = """
•× /purge - delete couples of messages together

"""

LOCK = """
•× /lock (query) : lock particular content in chat.
•× /unlock (query) : Unlock some content.
•× /locktypes : get all Queries for Locks

"""
GROP = """
•× /setgpic (reply photo) : keep Chat Photo of Group.

"""
ADMIN = """
•× /promote - to promote
•× /demote - to demote 
•× /kick - kick Someone 

"""
INFO = """
•× /info (reply/username/id) : get detailed info of user.
•× /id : get chat/user id.

"""
user = Config.BOT_USERNAME
hmm = (user[1:])

url1 = f"https://t.me/{hmm}/start?=start"
url2 =f"https://t.me/{hmm}?startgroup=True"

# <--MAIN CODES-->
@tgbot.on(events.NewMessage(pattern="/help"))
async def helpish(alphax):
        if MANAGER == "ON":
            if not alphax.is_private:
              await alphax.reply("Yep..SiR\nplease contact me in PM(^_^) To know More:)", buttons=[
                  [
                      Button.url("Cᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ Pᴍ! 🪂", url=url1)]
                  ])
            else:
              await tgbot.send_message(astro.chat_id, f"Hello There🧚...\n This is {BOT_NAME} I will help you to manage your groups! with BASIC modules check it out\n\nMY BASIC COMMANDS:/ping\n/help\n/repo\n\n\n αℓρнαχ \n S E R V I C E", buttons=[
                [
          Button.inline("BANS🚫", data="ben"),
          Button.inline("MUTES🤫", data="shut")
          ], 
          [
          Button.inline("PIN📌", data="pin"),
          Button.inline("PURGES💨", data="purge")
          ],
          [
            Button.inline("LOCKS🔒", data="lck"),
            Button.inline("GROUP EDITS⚙️", data="grpit")
          ],
          [
            Button.inline("INFORMATIONℹ️", data="ids"),
            Button.inline("ADMIN🧑‍✈️", data="admen")
          ],
          [
            Button.url("✙Add Me to your Group✙", url=url2)],
              ]
            )
        else:
           await tgbot.send_message(astro.chat_id, "**MASTER!!**\n __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")
        
    # Call backs <-->
@tgbot.on(events.callbackquery.CallbackQuery(data="admen"))
async def admen(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, ADMIN, buttons=[
      [
        Button.inline("»Bᴀᴄᴋ«", data="beck")
      ]
    ])
@tgbot.on(events.callbackquery.CallbackQuery(data="ben"))
async def ben(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, BAN, buttons=[
        [
          Button.inline("»Bᴀᴄᴋ«", data="beck")]
        ])
        
    
@tgbot.on(events.callbackquery.CallbackQuery(data="shut"))
async def shut(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, SHUTUP, buttons=[
        [
          Button.inline("»Bᴀᴄᴋ«", data="beck")]
        ])

@tgbot.on(events.callbackquery.CallbackQuery(data="pin"))
async def pin(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, PIN, buttons=[
        [
          Button.inline("»Bᴀᴄᴋ«", data="beck")]
        ])
        
        
@tgbot.on(events.callbackquery.CallbackQuery(data="purge"))
async def purge(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, PUR, buttons=[
        [
          Button.inline("»Bᴀᴄᴋ«", data="beck")]
        ])
        
@tgbot.on(events.callbackquery.CallbackQuery(data="lck"))
async def lck(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, LOCK, buttons=[
        [
          Button.inline("»Bᴀᴄᴋ«", data="beck")]
        ])
        
@tgbot.on(events.callbackquery.CallbackQuery(data="grpit"))
async def grpit(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, GROP, buttons=[
        [
          Button.inline("»Bᴀᴄᴋ«", data="beck")]
        ])
        
        
@tgbot.on(events.callbackquery.CallbackQuery(data="ids"))
async def ids(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, INFO, buttons=[
        [
          Button.inline("»Bᴀᴄᴋ«", data="beck")]
        ])
        
    # Back Button call back
@tgbot.on(events.callbackquery.CallbackQuery(data="beck"))
async def ids(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, f"Hello There🧚...\n This is {BOT_NAME} I will help you to manage your groups! with BASIC modules check it out\n\nMY BASIC COMMANDS:/ping\n/help\n/repo\n\n\n •αℓρнαχ• \n •S E R V I C E•", buttons=[
                [
          Button.inline("BANS🚫", data="ben"),
          Button.inline("MUTES🤫", data="shut")
          ], 
          [
          Button.inline("PIN📌", data="pin"),
          Button.inline("PURGES💨", data="purge")
          ],
          [
            Button.inline("LOCKS🔒", data="lck"),
            Button.inline("GROUP EDITS⚙️", data="grpit")
          ],
          [
            Button.inline("INFORMATIONℹ️", data="ids"),
            Button.inline("ADMIN🧑‍✈️", data="admen")
          ],
          [
            Button.url("✙Add Me to your Group✙", url=url2)],
              ]
            )
# @XD_OFFLINE
# Keep credits 
# Kanger == Fucked

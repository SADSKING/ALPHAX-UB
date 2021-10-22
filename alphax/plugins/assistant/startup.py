import asyncio 
import re
import os 
import html
import heroku3
import requests
from datetime import datetime
from telethon import events
from telethon import Button, events 
from alphax.plugins.assistant import *
from alphax.plugins import ASTRO
from alphax.plugins.assistant.sql.blacklist_sql import all_bl_users
from astro.plugins.assistant.sql.userbase_sql import add_to_userbase, present_in_userbase, full_userbase

from astro.config import Config 
from telegraph import Telegraph, upload_file


####  Config ####
PR_PIC = "https://telegra.ph/file/d1c714e19d3694f063659.jpg"
PM_TEXT = Config.PM_TEXT
PM_PIC = Config.PM_PIC
A_PIC = Config.A_PIC
A_TEXT = Config.A_TEXT
NAME = Config.NAME
HNDLR = Config.HNDLR
LOAD_MYBOT = Config.LOAD_MYBOT
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
BOT_PIC = Config.BOT_PIC if Config.BOT_PIC else None

OWNER_USERNAME = Config.OWNER_USERNAME
heroku_api = "https://api.heroku.com"
path = Config.TMP_DOWNLOAD_DIRECTORY
if not os.path.isdir(path):
    os.makedirs(path)
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]

### here 4 later purpose ###

# Lets Start #

@tgbot.on(events.NewMessage(pattern="/start"))
async def start(event):
    if event.chat_id == OWNER_ID:
        return
    target = event.sender_id
    if present_in_userbase(target):
        pass
    else:
        try:
            add_to_userbase(target)
        except BaseException:
            pass
    if LOAD_MYBOT == "False":
        if BOT_PIC:
            await tgbot.send_file(event.chat_id, BOT_PIC, caption=others, buttons=[
                [
                  Button.inline("What is This🧐", data="fck")
                ],
              ]
            )
        else:
            await tgbot.send_message(event.chat_id, others, buttons=[
                [
                  Button.inline("What is This🧐", data="fck")
                ],
              ]
            )
    elif LOAD_MYBOT == "True":
        if BOT_PIC:
            await tgbot.send_file(event.chat_id, BOT_PIC, caption=customtxt, buttons=[
                [
                  Button.inline("What is This🧐", data="fck")
                ],
              ]
            )
        else: 
            await tgbot.send_message(event.chat_id, customtxt, buttons=[
                [
                  Button.inline("What is this🧐?", data="fck")
                ],
              ]
            )
            
    # When Owner will start # 
    
@tgbot.on(events.NewMessage(pattern="/start", from_users=OWNER_ID))
async def start_by_owner(event):
    await tgbot.send_file(event.chat_id, PR_PIC, caption=ownerstart, buttons=[
          [
            Button.inline("PM Set-up⚙️", data="pmset"),
            Button.inline("Custom Set-up⚙️", data="change")
          ],
          [
            Button.inline("BOT PIC📷", data="groom")
          ],
          [
            Button.inline("BroadCast📡", data="broad")
          ],
          [
            Button.url("🔻Support 🔺", url="https://t.me/Alphax_HelpChat")],
            ],
          )
          
# BUTTONS DATA # 

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"fck")))
async def fck(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, f"This is คɭקђคא  UserBot for {OWNER_USERNAME} 😊 To protect him from scammers and lots more...!\n**IF YOU ALSO WANT FOR YOUR ACCOUNT DEPLOY NOW**\n **JOIN SUPPORT FOR HELP**", buttons=[
        [
          Button.url("Deploy Now🌌", url="https://github.com/Mohan745/ALPHAX-UB")
        ],
        [
          Button.url("Repository✨", url="https://github.com/Mohan745/ALPHAX-UB")
        ],
        [
          Button.url("🔻Support🔺", url="https://t.me/Alphax_HelpChat")
          ],
        ])
     
   
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"broad")))
async def broadcast(event):
    if event.sender_id != OWNER_ID:
        await event.answer("You can't use this bot")
        return
    await tgbot.send_message(event.chat_id, "Send the message you want to broadcast!\nSend /cancel to stop.")
    async with event.client.conversation(OWNER_ID) as conv:
        response = conv.wait_event(events.NewMessage(chats=OWNER_ID))
        response = await response
        themssg = response.message.message
    if themssg is None:
        await tgbot.send_message(event.chat_id, "An error has occured...")
    if themssg == "/cancel":
        await tgbot.send_message(event.chat_id, "Broadcast cancelled!")
        return
    targets = full_userbase()
    users_cnt = len(full_userbase())
    err = 0
    success = 0
    lmao = await tgbot.send_message(event.chat_id, "Starting broadcast to {} users.".format(users_cnt))
    start = datetime.now()
    for ok in targets:
        try:
            await tgbot.send_message(int(ok.chat_id), themssg)
            success += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            err += 1
            try:
                await tgbot.send_message(Config.PRIVATE_GROUP_ID, f"**Error**\n{str(e)}\nFailed for user: {chat_id}")
            except BaseException:
                pass
    end = datetime.now()
    ms = (end - start).seconds
    done_mssg = """
Broadcast completed!\n
Sent to `{}` users in `{}` seconds.\n
Failed for `{}` users.\n
Total users in bot: `{}`.\n
""".format(success, ms, err, users_cnt)
    await lmao.edit(done_mssg)
    try:
        await tgbot.send_message(Config.PRIVATE_GROUP_ID, f"#Broadcast\nCompleted sending a broadcast to {success} users.")
    except BaseException:
        await tgbot.send_message(event.chat_id, "Please add me to your Private log group for proper use.")
        
     
   
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmset")))
async def pmsettings(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, "Select What You wanna To do in PM settings\n**CHOOSE FROM BELOW:**", buttons=[
        [
          Button.inline("PM TEXT", data="pm_txt")
        ],
        [
          Button.inline("PM PIC", data="pm_pic")],
        ],
      )
     
    
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"change")))
async def pmsettings(event):
    await event.delete()
    await tgbot.send_message(event.chat_id, "Select what You wanted to edit in Alive settings\n**CHOOSE FROM BELOW:**", buttons=[
        [
          Button.inline("ALIVE TEXT", data="alv_txt")
        ],
        [
          Button.inline("ALIVE PIC", data="alv_pic")
        ],
        [
          Button.inline("COMMAND HNDLR", data="hndlr")
        ],
        [
          Button.inline("ALIVE NAME", data="alv_nme")
        ],
       ]
      )
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"alv_txt")))
async def a_txt(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        old_alv=Config.A_TEXT if Config.A_TEXT else "Default Alive message"
        astrobot="A_TEXT"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send the text which you want as your alive text.\nUse /cancel to cancel the operation.")
            response=conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response=await response
            themssg=response.message.message
            if themssg == None:
                await conv.send_message("Error!")
                return
            if themssg == "/cancel":
                return await conv.send_message("Cancelled!!")
                heroku_var=app.config()
            xx = await tgbot.send_message(event.chat_id, "Changing your Alive Message, please wait for a minute")
            heroku_var[astrobot]=f"{themssg}"
            mssg=f"Changed your alive text from\n`{old_alv}`\nto\n`{themssg}`\n"
            await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)
        
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"alv_pic")))
async def pmpic(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        old_pic= A_PIC if A_PIC else "Default Picture..."
        astrobot="A_PIC"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send the new Telegraph Link of PICTURE WHICH YOU WANT TO USE\n\nLink must be in `https://telegr.ph/....`\nUse /cancel to cancel the operation.")
            response=conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response=await response
            themssg=response.message.message
            if themssg == None:
                await conv.send_message("Error!")
                return
            if themssg == "/cancel":
                await conv.send_message("Cancelled!!")
                return
            heroku_var=app.config()
            xx = await tgbot.send_message(event.chat_id, "Changing Your ALIVE_PIC❤️Give me 3min..and Check Your Private group😁")
            heroku_var[astrobot]=f"{themssg}"
            mssg=f"Changed your ALIVE PIC FROM\n`{old_pic}`\nto\n`{themssg}`\n"
            await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)
        
        
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"alv_nme")))
async def a_txt(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        old_alv= NAME if NAME else "Default Alive name "
        astrobot="NAME"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send the text which you want as your ALIVE Name!\nUse /cancel to cancel the operation.")
            response=conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response=await response
            themssg=response.message.message
            if themssg == None:
                await conv.send_message("Error!")
                return
            if themssg == "/cancel":
                await conv.send_message("Cancelled!!")
                return
            heroku_var=app.config()
            xx = await tgbot.send_message(event.chat_id, "Changing your Alive Name, please wait for a minute")
            heroku_var[astrobot]=f"{themssg}"
            mssg=f"Changed your Name from\n`{old_alv}`\nto\n`{themssg}`\n"
            await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)
        
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pm_txt")))
async def a_txt(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        old_alv= PM_TEXT if PM_TEXT else "Default PMSecurity message"
        telebot="PM_TEXT"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send the text which you want as your PMSecurity Message!\nUse /cancel to cancel the operation.")
            response=conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response=await response
            themssg=response.message.message
            if themssg == None:
                await conv.send_message("Error!")
                return
            if themssg == "/cancel":
                await conv.send_message("Cancelled!!")
                return
            heroku_var=app.config()
            xx = await tgbot.send_message(event.chat_id, "Changing your PMSecurity Message, please wait for a minute")
            heroku_var[telebot]=f"{themssg}"
            mssg=f"Changed your PMsecurity Message from\n`{old_alv}`\nto\n`{themssg}`\n"
            await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)
        
  
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pm_pic")))
async def pmpic(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        old_pic= PM_PIC if PM_PIC else "Default Picture...!"
        astrobot="PM_PIC"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send the new Telegraph Link of PICTURE WHICH YOU WANT TO USE\n\nLink must be in` https://telegr.ph/....`\nUse /cancel to cancel the operation.")
            response=conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response=await response
            themssg=response.message.message
            if themssg == None:
                await conv.send_message("Error!")
                return
            if themssg == "/cancel":
                await conv.send_message("Cancelled!!")
                return
            heroku_var=app.config()
            xx = await tgbot.send_message(event.chat_id, "Changing Your PM_PIC❤️Give me 3min..and Check Your Private group😁")
            heroku_var[astrobot]=f"{themssg}"
            mssg=f"Changed your PM_PIC from\n`{old_pic}`\nto\n`{themssg}`\n"
            await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)
        
        
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"hndlr")))
async def a_txt(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        old_hndlr= HNDLR if HNDLR else "Default Command Handler ."
        astrobot="HNDLR"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send the new Command Handlr which you wanna to use to run commands!\nUse /cancel to cancel the operation.")
            response=conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response=await response
            themssg=response.message.message
            if themssg == None:
                await conv.send_message("Error!")
                return
            if themssg == "/cancel":
                await conv.send_message("Cancelled!!")
                return
            heroku_var=app.config()
            xx = await tgbot.send_message(event.chat_id, "Changing your Command Handler, please wait for a minute")
            heroku_var[astrobot]=f"{themssg}"
            mssg=f"Changed your Handlr from\n`{old_hndlr}`\nto\n`{themssg}`\n"
            await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"groom")))
async def groom(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        old_pic= BOT_PIC if BOT_PIC else "Default Picture...!"
        astrobot="BOT_PIC"
        if Config.HEROKU_APP_NAME is not None:
            app=Heroku.app(Config.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send the new Telegraph Link of PICTURE WHICH YOU WANT TO USE\n\nLink must be in` https://telegr.ph/....`\nUse /cancel to cancel the operation.")
            response=conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response=await response
            themssg=response.message.message
            if themssg == None:
                await conv.send_message("Error!")
                return
            if themssg == "/cancel":
                await conv.send_message("Cancelled!!")
                return
            heroku_var=app.config()
            xx = await tgbot.send_message(event.chat_id, "Changing Your BOT_PIC ❤️Give me 3min..and Check Your Private group😁")
            heroku_var[astrobot]=f"{themssg}"
            mssg=f"Changed your BOT_PIC from\n`{old_pic}`\nto\n`{themssg}`\n"
            await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)

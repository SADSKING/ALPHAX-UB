import time
from datetime import datetime
from telethon import events
from alphax.config import Config 

MANAGER = Config.MANAGER

@tgbot.on(events.NewMessage(pattern="/ping"))
async def ping(event):
    if MANAGER == "ON":
      if event.fwd_from:
         return
      start = datetime.now()
      end = datetime.now()
      ms = (end - start).microseconds / 1000
      await event.reply(f"""
⎝⎝•𝙋𝙊𝙉𝙂•⎠⎠\n
. 　   ♡＿＿＿
　　   ∥  MY MS |
　　   ∥`{ms}`s |
　　   ∥￣￣￣￣
 (✿◕‿◕)
•คɭקђคא เร คɭเשє•

""", 
)
    else:
      await event.reply("Master Please Enable Manager by using `.set Config MANAGER ON`")

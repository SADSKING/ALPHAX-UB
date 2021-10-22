#<--imports--> 
from telethon import Button
from telethon import events
from alphax.config import Config 
# <--Main Links--> #
REPO = "https://github.com/Mohan745/ALPHAX-UB"
SUPPORT = "https://t.me/Alphax_HelpChat"
UPDATES = "https://t.me/Alphax_UserBot"
PLUG = "https://t.me/Alphax_Plugins"
BOTS = "https://t.me/Xd_OFFLINE"

# <-- Config --> #
MANAGER = Config.MANAGER
BOT_NAME = Config.BOT_NAME if Config.BOT_NAME else "คɭקђคא ๏ Assistant 🧚"
user = Config.BOT_USERNAME
hmm = (user[1:])

urll = f"https://t.me/{hmm}/start?=start"

# <--Notes--> #
MSG = f"Hey There My Name is {BOT_NAME}\nBelow is My All Links and More!\nCheck it out😊"

@tgbot.on(events.NewMessage(pattern="/repo"))
async def repo(astro):
      if MANAGER == "ON":
            if not astro.is_private:
              await astro.reply("Hey There🧞‍♂️\nContact me in PM!", buttons=[
                  [
                    Button.url("🧞‍♂️ᴄᴏɴᴛᴀᴄᴛ  ᴍᴇ  ɪɴ  ᴘᴍ!🧞‍♂️", url=urll)],
                        ]
                      )
            else:
                await tgbot.send_message(astro.chat_id, MSG, buttons=[
            [
              Button.url("Repository✨", url=REPO)
            ],
            [
              Button.url("αℓρнαχ๏ sᴜᴘᴘ๏ʀᴛ", url=SUPPORT),
              Button.url("คɭקђคא υsєяъ๏т", url=UPDATES)
            ],
            [
              Button.url("αℓρнαχ๏ ᴘʟᴜɢɪɴs", url=PLUG)
            ],
            [
              Button.url("αℓρнαχ๏ ɮѳτs", url=BOTS)],
              ]
            )
      else:
        await tgbot.send_message(astro.chat_id, "**Master!**\n__Master Please Enable MANAGER__ By using `.set Config MANAGER ON`")
        
# ©XD_OFFLINE
# Alphax_UserBot
# Keep Credits Kanger

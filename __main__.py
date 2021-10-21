import glob
from alphax import bot
from sys import argv
from telethon import TelegramClient
from alphax.config import Config
from alphax.utils import load_module, start_assistant, load_pmbot
from pathlib import Path
import telethon.utils
from alphax import CMD_HNDLR
# Configs

GROUP = Config.PRIVATE_GROUP_ID
BOTNAME = Config.BOT_USERNAME
LOAD_MYBOT = Config.LOAD_MYBOT
BOT_USERNAME = Config.BOT_USERNAME
OWNER_USERNAME = Config.OWNER_USERNAME 

async def add_bot(bot_token):
    await bot.start(bot_token)
    bot.me = await bot.get_me()
    bot.uid = telethon.utils.get_peer_id(bot.me)


async def startup_log_all_done():
    try:
        await bot.send_message(GROUP, f"Hey..{OWNER_USERNAME} ꍏ↳ρ♄ꍏ⌘ ♗∫ ᕲ€ρ↳⊙⚧€ᕲ\nnow you are 100% Safe By alphax😉\nUSE `.alive` To check me😁\n\n Add {BOT_USERNAME} To get Notifications Related to Alphax-UB \n~Enjoy~\n\n~ @ALPHAX_HELPCHAT")
    except BaseException:
        print("Either PRIVATE_GROUP_ID is wrong or you have left the group.")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    if Config.BOT_USERNAME is not None:
        print("Initiating Inline Bot")
        # ForTheGreatrerGood of beautification
        bot.tgbot = TelegramClient(
            "BOT_TOKEN",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH
        ).start(bot_token=Config.BOT_TOKEN)
        print("Initialisation finished, no errors")
        print("Starting Userbot")
        bot.loop.run_until_complete(add_bot(Config.BOT_USERNAME))
        print("Startup Completed")
    else:
        bot.start()

path = 'astro/plugins/*.py'
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))

print("alphax has been deployed! ")

print("Setting up TGBot")
path = "alphax/plugins/assistant/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        start_assistant(shortname.replace(".py", ""))

if LOAD_MYBOT == "True":
    path = "alphax/plugins/assistant/pmbot/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            load_pmbot(shortname.replace(".py", ""))
    print("TGBot set up completely!")


print("λᏓᎵ𐒅λ𐒎 ᎥᎴ Ꮷ𐒢ᎵᏓ𐒀𐒍𐒢Ꮷ!")
print("||•||°••°αℓρɦαא υsєяъ๏т°••°||•||")
print("~jσıη sυρρσят ƒσя мσяє~") 
print("✗⌜◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉⌟✗")
print("⚔°•°•°•°•°•D Visit @ALPHAX_HELPCHAT•°•°•°•°•°•⚔")
print("✗⌜◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉◎◉⌟✗")

bot.loop.run_until_complete(startup_log_all_done())

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()

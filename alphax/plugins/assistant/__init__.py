
from astro.plugins import ALPHAX, OWNER_ID
import time
from datetime import datetime
from alphax.config import Config 

# OTHER STARTED WHILE DISABLE BOT 
others = """
Hi there. I am {}'s bot. Nice to see you here
""".format(ASTRO)
# Ok you know 

if Config.PMBOT_START_MSSG is None:
    MSSG = """
Hi there, I am {}'s personal bot.
I am Helper BoT 😁
Contact him from me Just send me Your Message 😌 I will forward him 
""".format(ALPHAX)
else:
    MSSG = Config.PMBOT_START_MSSG
customtxt = MSSG

ownerstart = """
Hi {} How are you master 
select What can i do for You Today😁
""".format(ALPHAX)

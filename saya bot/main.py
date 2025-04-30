from telethon import *
import config
from modules.help import *
from modules.scraper import *
from modules.ping import *
from modules.afk import *
from modules.purge import *
from modules.uwufy import *
from modules.globalBan import *

client = TelegramClient(session="Saya",
    api_id=config.API_ID,
    api_hash=config.API_HASH)


register_help(client)
register_ping(client)
register_afk(client)
register_scraper(client)
register_purge(client)
register_uwuify(client)
register_gban(client)
client.start()
client.run_until_disconnected()

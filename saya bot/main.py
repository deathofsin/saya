from telethon import *
import config
from modules.help import *
from modules.scraper import *
from modules.ping import *
from modules.afk import *
from modules.purge import *
from modules.uwufy import *
from modules.globalBan import *
from modules.wife import *
from modules.admin import *



preinstall_db()
client = TelegramClient(session="Saya",
    api_id=config.API_ID,
    api_hash=config.API_HASH)


register_addwife(client)
register_showwifes(client)
register_removewife(client)
register_help(client)
register_ping(client)
register_afk(client)
register_scraper(client)
register_purge(client)
register_uwuify(client)
register_gban(client)
register_add_admin(client)
register_remove_admin(client)
register_showadmins(client)
client.start()
client.run_until_disconnected()

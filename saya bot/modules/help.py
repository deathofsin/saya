from telethon import *
import random
from utils.functions import delete_message

async def help(client, event):
    try:
        await delete_message(client, event)
        photos = await client.get_profile_photos('me')
        if photos:
            await client.send_file(event.chat_id, photos[0], caption = """⏝̅⏝̅⏝̅ ୨ ♱ ୧ ⏝̅⏝̅⏝̅
Saya Bot - <a href="https://github.com/deathofsin/saya/blob/main/commands.txt">Commands List</a>""", parse_mode='html')

    except Exception as e:
        me = await client.get_me()
        await client.send_message(me, f"Error: {e}")


def register_help(client):
    @client.on(events.NewMessage(pattern='^\.help', outgoing=True))
    async def help_handler(event):
        await help(client,event)
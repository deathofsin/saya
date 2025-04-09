from telethon import *
from utils.functions import *
import random

async def ping(client, event):
    try:
        await delete_message(client, event)
        response = ["Online🌐", "Im here💢"]
        rand_response = random.choice(response)
        await event.reply(f"{rand_response}")
    except Exception as a:
        me = await client.get_me()
        await client.send_message(me, f"Errore: {a}")


def register_ping(client):
    @client.on(events.NewMessage(pattern='^\.ping', outgoing=True))
    async def ping_handler(event):
        await ping(client,event)
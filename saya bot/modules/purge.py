from telethon import TelegramClient, events
from utils.functions import *

async def purge(client, event, chatid):
    try:
        await delete_message(client, event)
        async for message in client.iter_messages(chatid):
            await client.delete_messages(chatid, message.id)
       
        await client.send_message(event.chat_id, """all messages have been deleted""")
    except Exception as e:
        me = await client.get_me() 
        await client.send_message(me.id, f"Error: {e}")


def register_purge(client):
    @client.on(events.NewMessage(pattern="^\.purge", outgoing=True))
    async def purge_handler(event):
        chat_id = event.chat_id
        await purge(client, event, chat_id)
from telethon import *


async def delete_message(client, event): 
    await client.delete_messages(event.chat_id, [event.message.id])
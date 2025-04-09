from telethon.tl.functions.account import UpdateProfileRequest
from utils.functions import delete_message
from telethon import *

inactive = False

async def afk(client, event):
    try:
        await delete_message(client, event)
        global inactive
        args = event.message.text.split()
        if len(args) < 2:
            await event.reply("Please use 'active' to activate AFK or 'disable' to disable AFK.")
            return

        choice = args[1].lower()
        if choice == "active":
            inactive = True
            await client(UpdateProfileRequest(
                last_name="AFK"
            ))
            await event.reply("AFK mode activated.")
        elif choice == "disable":
            inactive = False
            await client(UpdateProfileRequest(
                last_name=""
            ))
            await event.reply("AFK mode disabled.")
        else:
            await event.reply("Invalid option. Use 'active' or 'disable'.")
    except Exception as e:
        me = await client.get_me()
        await client.send_message(me, f"Error: {e}")


def register_afk(client):
    @client.on(events.NewMessage(pattern='^\.afk', outgoing=True))
    async def afk_handler(event):
        await afk(client,event)
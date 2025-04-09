from telethon import *
from utils.functions import delete_message
import csv
import os

async def scraper(client, event):
    try:
        await delete_message(client, event)
        args = event.message.text.split()
        if len(args) < 2:
            await event.reply("Please provide a username Group or ID Group.")
            return
        group = args[1]
        users = await client.get_participants(group)
        with open(f"{group}.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Surname", "Username", "Phone"])
            
            for user in users:
                writer.writerow([
                    user.id,
                    user.first_name or "",
                    user.last_name or "",
                    user.username or "",
                    user.phone or ""
                ])
        await client.send_file("me", f"{group}.csv", caption=f"Here is the list of users in the group: {group}")
        os.remove(f"{group}.csv")
    except Exception as e:
        me = await client.get_me()
        await client.send_message(me, f"Error: {e}")

def register_scraper(client):
    @client.on(events.NewMessage(pattern='^\.scraper', outgoing=True))
    async def scraper_handler(event):
        await scraper(client,event)
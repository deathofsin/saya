from telethon import TelegramClient, events
import sqlite3
from utils.admin import is_admin


async def delete_message(client, event):
    await client.delete_messages(event.chat_id, [event.message.id])


async def add_admin(client, event, username):
    try:
        await delete_message(client, event)
        user = await client.get_entity(username)
        user_username = user.username
        user_id = user.id
        conn = sqlite3.connect("database/admin.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, username TEXT)")
        cur.execute("INSERT INTO admins (id, username) VALUES (?, ?)",(user_id, username))
        conn.commit()
        path = "https://i.pinimg.com/originals/f3/43/61/f34361e6d646971ce7490244ab96c7b6.gif"
        await client.send_file(event.chat_id, path, caption=f"@{user_username} has been added as admin.")
    except Exception as e:
        me = await client.get_me()
        await client.send_message(me.id, f"Error: {e}")


def register_add_admin(client):
    @client.on(events.NewMessage(pattern='^\.addadmin(?: |$)(.*)', outgoing=True))
    async def add_admin_handle(event):
        parts = event.message.text.split(" ", 1)
        if len(parts) < 2:
            await event.reply("Correct Syntax: .addadmin <username>")
            return
        username = parts[1]
        await add_admin(client, event, username)



async def remove_admin(client, event, username):
    try:
        await delete_message(client, event)
        user = await client.get_entity(username)
        user_username = user.username
        user_id = user.id
        conn = sqlite3.connect("database/admin.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM admins WHERE id = ?", (user_id,))
        path = "https://i.pinimg.com/originals/f3/43/61/f34361e6d646971ce7490244ab96c7b6.gif"
        await client.send_file(event.chat_id, path, caption=f"@{user_username} has been removed as admin.")
    except Exception as e:
        me = await client.get_me()
        await client.send_message(me.id, f"Error: {e}")
    
def register_remove_admin(client):
    @client.on(events.NewMessage(pattern='^\.deladmin(?: |$)(.*)', outgoing=True))
    async def remove_admin_handle(event):
        parts = event.message.text.split(" ", 1)
        if len(parts) < 2:
            await event.reply("Correct Syntax: .deladmin <username>")
            return
        username = parts[1]
        await remove_admin(client, event, username)


async def get_admins():
    try:
        conn = sqlite3.connect('database/admin.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM admins")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Errore: {e}")
        return[]
    

async def showadmins(client, event):
    try:
        if is_admin(event.sender_id):
            await delete_message(client, event)
            admins = await get_admins()
            response = f"here are the admins of @{event.sender.username}:\n\n"
            if admins:
                for entry in admins:
                    response += f"ID: <code>{entry[0]}</code>, Username: <code>{entry[1]}</code>\n"
                await client.send_message(event.chat_id, response, parse_mode="html")
            else:
                await client.send_message(event.chat_id, "There are no admins.")
    except Exception as e:
        print(f"Errore: {e}")
        await client.send_message(event.chat_id, f"Error: {e}")

def register_showadmins(client):
    @client.on(events.NewMessage(pattern='^\.showadmins'))
    async def handle_showadmins(event):
        if is_admin(event.sender_id):
            await showadmins(client, event)


from telethon import *
import sqlite3
from utils.functions import delete_message
from utils.admin import is_admin

async def addwife(client, event, username):
    try:
        await delete_message(client, event)
        user_entity = await client.get_input_entity(username) 
        user_id = user_entity.user_id
        conn = sqlite3.connect('database/wifes.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS wifes (id INTEGER PRIMARY KEY, username TEXT)")
        cur.execute("INSERT INTO wifes (id, username) VALUES (?, ?)",(user_id, username))
        path = "https://i.imgur.com/cd06qM9.gif"
        await client.send_file(event.chat_id, path, caption=f"""the user: {username} she became the wife of @{event.sender.username}.""")
        conn.commit()
        conn.close()
    except Exception as a:
        me = await client.get_me()
        await client.send_message(me.id, f"Error: {a}")
    

def register_addwife(client):
    @client.on(events.NewMessage(pattern='\.addwife(?: |$)(.*)', outgoing=True))
    async def handle_addwife(event):
        parts = event.message.text.split(" ", 2)
        if len(parts) < 2:
            await event.reply("correct syntax: .addwife <username>")
            return
        username = parts[1]
        await addwife(client, event, username)



async def get_wifes():
    try:
        conn = sqlite3.connect('database/wifes.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM wifes")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Errore: {e}")
        return[]

async def showwifes(client, event):
    try:
            await delete_message(client, event)
            wifes = await get_wifes()
            response = f"Here are the wives of @{event.sender.username}:\n\n"
            if wifes:
                for entry in wifes:
                    response += f"ID: <code>{entry[0]}</code>, Username: <code>{entry[1]}</code>\n"
                await client.send_message(event.chat_id, response, parse_mode="html")
            else:
                await client.send_message(event.chat_id, "There are no wives.")
    except Exception as e:
        print(f"Errore: {e}")
        await client.send_message(event.chat_id, f"Error: {e}")

def register_showwifes(client):
    @client.on(events.NewMessage(pattern='^\.showwifes'))
    async def handle_showwifes(event):
        if is_admin(event.sender_id):
            await showwifes(client, event)



async def removewife(client, event, username):
    try:
        await delete_message(client, event)
        user_entity = await client.get_input_entity(username)
        user_id = user_entity.user_id
        conn = sqlite3.connect('database/wifes.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM wifes WHERE id = ?", (user_id,))
        path = "https://i.imgur.com/cd06qM9.gif"
        await client.send_file(event.chat_id, path, caption=f"""the user: {username} she is no longer the wife of @{event.sender.username}.""")
        conn.commit()
        conn.close()
    except Exception as e:
        me = await client.get_me()
        await client.send_message(me.id, f"Error: {e}")


def register_removewife(client):
    @client.on(events.NewMessage(pattern="^\.delwife(?: |$)(.*)", outgoing=True))
    async def handle_removewife(event):
        parts = event.message.text.split(" ", 2)
        if len(parts) < 2:
            await event.reply("Correct Syntax: .delwife <username>")
            return
        username = parts[1]
        await removewife(client, event, username)

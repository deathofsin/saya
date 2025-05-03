from telethon import *
from utils.functions import delete_message
from utils.admin import is_admin
async def help(client, event):
    try:
        await delete_message(client, event)
        photos = await client.get_profile_photos('me')
        me = await client.get_me()
        name = me.first_name if me.first_name else "No name"
        last_name = me.last_name if me.last_name else "No last name"
        username = me.username if me.username else "No username"
        if photos:
            await client.send_file(event.chat_id, photos[0], caption = f"""Saya Bot - <a href="https://github.com/deathofsin/saya/blob/main/commands.txt">Commands List</a>
✦ First Name: {name}
✦ Last Name: {last_name}
✦ Username: @{username}""", parse_mode='html')
        else:
             await client.send_file(event.chat_id, photo="https://64.media.tumblr.com/58190bc47e00c135396518fa16fab66d/tumblr_oe3g8rveLG1th93f0o1_540.gif", caption = f"""Saya Bot - <a href="https://github.com/deathofsin/saya/blob/main/commands.txt">Commands List</a>
✦ First Name: {name}
✦ Last Name: {last_name}
✦ Username: @{username}""", parse_mode='html')

    except Exception as e:
        me = await client.get_me()
        await client.send_message(me, f"Error: {e}")


def register_help(client):
    @client.on(events.NewMessage(pattern='^\.help'))
    async def help_handler(event):
        if is_admin(event.sender_id):
            await help(client,event)
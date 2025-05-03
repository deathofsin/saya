import random
from telethon import *
from utils.functions import *
from utils.admin import is_admin

def uwuify(text):
    try:
        text = text.lower()
        text = text.replace("r", "w").replace("l", "w")
        text = text.replace("no", "nyo").replace("mo", "myo")
        text = text.replace('na', 'nya').replace('ne', 'nye').replace('ni', 'nyi')
        text = text.replace("nu", "nyu").replace("ne", "nye")
        text = text.replace("ka", "nya").replace("ke", "nye").replace("ki", "nyi")
        text = text.replace("ku", "nyu").replace("ke", "nye")
        text = text.replace("ra", "wa").replace("re", "we").replace("ri", "wi")
        text = text.replace("ru", "wu").replace("re", "we")
        text = text.replace("ka", "nya").replace("ke", "nye").replace("ki", "nyi")
        faces = [
            "UwU", "OwO", "UwU", "OwO", "UwU", "OwO",
            "Nyaa~", "Nya~", "Nyaa~", "Nya~", "Nyaa~", "Nya~"
        ]
        text += " " + random.choice(faces)
        return text
    except Exception as e:
        print(f"Error in uwufy function: {e}")        

async def uwu(client, event):
    try:
        await delete_message(client, event)
        args = event.message.text.split()
        if len(args) < 2:
            await event.reply("Please provide a message to uwu.")
            return
        message = " ".join(args[1:])
        uwufied_message = uwuify(message)
        await event.reply(uwufied_message)
    except Exception as e:
        me = await client.get_me()
        await client.send_message(me, f"Error: {e}")


def register_uwuify(client):
    @client.on(events.NewMessage(pattern='^\.uwu', outgoing=True))
    async def uwuify_handler(event):
        if is_admin(event.sender_id):
            await uwu(client, event)
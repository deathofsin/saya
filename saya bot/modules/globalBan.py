from telethon import *
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.errors.rpcerrorlist import UserNotMutualContactError
from utils.functions import delete_message
from telethon.tl.types import InputMediaPhotoExternal


ban_rights = ChatBannedRights(
    until_date=None,
    view_messages=True
)

async def gban(client, event):
    try:
        await delete_message(client, event)
        username = event.message.text.split()[1]
        if not username:
            await event.reply("Please provide a username or user ID.")
            return
        target = await client.get_input_entity(username)
        if not target:
            await event.reply("User not found.")
            return
        me = await client.get_me()
        banned = []
        failed = []

        async for dialog in client.iter_dialogs():
            if dialog.is_channel and dialog.is_group:
                try:
                    participant = await client(GetParticipantRequest(dialog.id, me.id))
                    if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                        await client(EditBannedRequest(dialog.id, target, ban_rights))
                        banned.append(dialog.title)
                except UserNotMutualContactError:
                    failed.append(dialog.title)
                except Exception:
                    failed.append(dialog.title)

        result = f"𝖦𝗅𝗈𝖻𝖺𝗅 𝖻𝖺𝗇 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾d.\n\n" + f"{username} 𝘉𝘢𝘯𝘯𝘦𝘥 𝘧𝘳𝘰𝘮\n" + "⏝̅⏝̅⏝̅ ୨ ♱ ୧ ⏝̅⏝̅⏝̅\n" + "\n".join(f"✦ {item}" for item in banned)
        if failed:
            result += f"\n\n𝘍𝘢𝘪𝘭𝘦𝘥 𝘧𝘳𝘰𝘮\n" + "⏝̅⏝̅⏝̅ ୨ ♱ ୧ ⏝̅⏝̅⏝̅\n" + "\n".join(f"✦ {item}" for item in failed)

        media_url = "https://64.media.tumblr.com/58190bc47e00c135396518fa16fab66d/tumblr_oe3g8rveLG1th93f0o1_540.gif"
        await client.send_file(event.chat_id, media_url, caption=result)

    except Exception as e:
        me = await client.get_me()
        await client.send_message(me, f"Error: {e}")

def register_gban(client):
    @client.on(events.NewMessage(pattern='^\.gban', outgoing=True))
    async def gban_handler(event):
        await gban(client, event)
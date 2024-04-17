from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_join_channels_keyboard():

    channel_links = [
        "https://t.me/+sklWTNcPFx4zNTE1",
        "https://t.me/Colourtrading"
    ]
    keyboard = []
    grouped_links = list(zip(*[iter(channel_links)]*1))
    
    for group in grouped_links:
        row = []
        for link in group:
            row.append(InlineKeyboardButton("", url=link))
        keyboard.append(row)
    
    
    if len(channel_links) % 2 == 1:
        keyboard.append([InlineKeyboardButton("👉🏻 ꜱᴜʙꜱᴄʀɪʙᴇ ɴᴏᴡ 👈🏻", url=channel_links[-1])])
    
    
    keyboard.append([InlineKeyboardButton("ɴᴇxᴛ ➡️", callback_data="check_joined")])
    
    return InlineKeyboardMarkup(keyboard)

async def check_user_joined_channels(client, user_id, required_channel_ids):
    for channel_id in required_channel_ids:
        try:
            member = await client.get_chat_member(channel_id, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except Exception:
            return False
    return True

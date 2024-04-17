import asyncio
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InlineKeyboardMarkup
from pyrogram.errors import FloodWait

from handlers.database import db

app = None

ALLOWED_USER_IDS = [6322577824, 5693070387]
def setup_broadcast(application):
    global app
    app = application

    @app.on_message(filters.command("broadcast") & filters.user(ALLOWED_USER_IDS))
    async def broadcast_message(client, message):
        if not message.reply_to_message:
            return await message.reply_text("Please reply to a message with content to broadcast.")

        # Handling different types of messages
        if message.reply_to_message.text:
            content = message.reply_to_message.text
            markup = message.reply_to_message.reply_markup if isinstance(message.reply_to_message.reply_markup, InlineKeyboardMarkup) else None
        elif message.reply_to_message.photo:
            content = InputMediaPhoto(message.reply_to_message.photo.file_id)
        elif message.reply_to_message.video:
            content = InputMediaVideo(message.reply_to_message.video.file_id)
        else:
            return await message.reply_text("Unsupported message type for broadcasting.")

        # Fetch user ids from database
        user_ids = await fetch_all_user_ids()
        sent, failed = 0, 0
        for user_id in user_ids:
            try:
                if isinstance(content, (InputMediaPhoto, InputMediaVideo)):
                    await app.send_media_group(user_id, [content])
                else:
                    await app.send_message(user_id, content, reply_markup=markup)
                sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {str(e)}")
                failed += 1

        await message.reply_text(f"Broadcast completed: Sent to {sent} users, {failed} failed.")

async def fetch_all_user_ids():
    """Fetch all user IDs from the users collection in the database."""
    users_collection = db['users']
    all_users = users_collection.find({}, {'user_id': 1, '_id': 0})
    return [user['user_id'] for user in all_users]

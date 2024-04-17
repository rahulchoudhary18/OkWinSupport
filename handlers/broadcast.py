import asyncio
from pyrogram import Client, filters
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
            return await message.reply_text("Please reply to a text or image message for broadcasting.")

        
        content_type = 'photo' if message.reply_to_message.photo else 'text'
        file_id = message.reply_to_message.photo.file_id if message.reply_to_message.photo else None
        text_content = message.reply_to_message.text if message.reply_to_message.text else None
        caption = message.reply_to_message.caption if message.reply_to_message.caption else None
        reply_markup = message.reply_to_message.reply_markup if hasattr(message.reply_to_message, 'reply_markup') else None

        
        user_ids = await fetch_all_user_ids()

        sent, failed = 0, 0
        for user_id in user_ids:
            try:
                if content_type == 'photo':
                    await app.send_photo(chat_id=user_id, photo=file_id, caption=caption, reply_markup=reply_markup)
                else:
                    await app.send_message(chat_id=user_id, text=text_content, reply_markup=reply_markup)
                sent += 1
                await asyncio.sleep(0.2)  # Sleep to manage rate limits
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception as e:
                #print(f"Failed to send message to {user_id}: {str(e)}")
                failed += 1

        await message.reply_text(f"Broadcast completed: Sent to {sent} users, {failed} failed.")

async def fetch_all_user_ids():
    """Fetch all user IDs from the users collection in the database."""
    users_collection = db['users']
    all_users = users_collection.find({}, {'user_id': 1, '_id': 0})
    return [user['user_id'] for user in all_users]

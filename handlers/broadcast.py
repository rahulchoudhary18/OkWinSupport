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
            return await message.reply_text("Please reply to a message with /broadcast to send it.")
        
        # Fetch all user IDs from the database
        user_ids = await fetch_all_user_ids()
        
        # Getting details from the replied message
        from_chat_id = message.chat.id
        message_id = message.reply_to_message.message_id

        sent, failed = 0, 0
        for user_id in user_ids:
            try:
                await app.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=message_id)
                sent += 1
                await asyncio.sleep(0.3)
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

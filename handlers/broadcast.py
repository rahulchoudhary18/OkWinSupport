import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from handlers.database import db

app = None

def setup_broadcast(application):
    global app
    app = application

@app.on_message(filters.command("broadcast") & filters.user(SUDOERS))
async def broadcast_message(client, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("Usage: /broadcast <message> or reply to a message with /broadcast")

    query = message.text.split(None, 1)[1] if len(message.command) >= 2 else None
    if message.reply_to_message:
        content = message.reply_to_message.text
    else:
        content = query

    if not content:
        return await message.reply_text("Error: No content to broadcast.")

    options = message.text.split()
    pin = '-pin' in options
    pin_loud = '-pinloud' in options

    user_ids = await fetch_all_user_ids()
    sent, failed = 0, 0
    for user_id in user_ids:
        try:
            msg = await app.send_message(user_id, content)
            if pin:
                await msg.pin(disable_notification=not pin_loud)
            sent += 1
            await asyncio.sleep(0.2)  # Prevent rate limits
        except FloodWait as e:
            await asyncio.sleep(e.x)  # Handle flood wait
        except Exception as e:
            print(f"Failed to send message to {user_id}: {str(e)}")
            failed += 1

    await message.reply_text(f"Broadcast completed: Sent to {sent} users, {failed} failed.")

async def fetch_all_user_ids():
    """ Fetch all user IDs from the users collection in the database. """
    users_collection = db['users']
    all_users = users_collection.find({}, {'user_id': 1, '_id': 0})
    return [user['user_id'] for user in all_users]

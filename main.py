from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import config
import logging
from handlers.mustjoin import check_user_joined_channels, generate_join_channels_keyboard

app = Client("bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

async def start(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_full_name = message.from_user.first_name
    if message.from_user.last_name:
        user_full_name += ' ' + message.from_user.last_name
    if await check_user_joined_channels(client, user_id, config.REQUIRED_CHANNEL_IDS):
        welcome_message = (
            "**👀 𝗧𝗲𝗹𝗹 𝗺𝗲 𝗛𝗼𝘄 𝗰𝗮𝗻 𝗜 𝗵𝗲𝗹𝗽 𝘆𝗼𝘂?**\n"
            "**🤝 मैं आपकी कैसे मदद कर सकती हूँ?**\n\n"
            "**💡ꜰɪʀꜱᴛ ꜱᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴜɪᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ᴀɴᴅ ɪꜰ ʏᴏᴜ ɴᴏᴛ ʀᴇɢɪꜱᴛᴇʀ ᴜɴᴅᴇʀ ᴏꜰꜰɪᴄɪᴀʟ(ᴍʏ) ʟɪɴᴋ ᴏʀ ɪɴ ᴍʏ ᴛᴇᴀᴍ ᴛʜᴇɴ ᴅᴏɴ'ᴛ ᴡᴀꜱᴛᴇ ᴏᴜʀ ᴛɪᴍᴇ.**\n\n"
            "**☞ Rᴇɢɪsᴛᴇʀ Wɪᴛʜ https://bdgwin.com/#/register?invitationCode=48854928**\n\n"
            "**👋 Eᴀʀɴ Dᴀɪʟʏ 2000₹-5000₹ Vɪᴀ Pʟᴀʏɪɴɢ Eᴀsʏ Gᴀᴍᴇs💰**\n\n"
            "**ᴛʜᴀɴᴋ ʏᴏᴜ 😘😘**\n"
            "**────────────────────────────**"
        )
          
        photo_url = "https://telegra.ph/file/a3852757146a2c0fcc184.jpg"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʀᴇᴄʜᴀʀɢᴇ / ᴡɪᴛʜᴅʀᴀᴡᴀʟ ɪꜱꜱᴜᴇ", url="https://t.me/lauraBDG66666")],
            [InlineKeyboardButton("ᴠɪᴘ ᴄʜᴀɴɴᴇʟ", url="https://t.me/+Fp_scQvsGKsyZDhl")],
            [InlineKeyboardButton("ʙᴇᴄᴏᴍᴇ ᴀɢᴇɴᴛ 🤵‍♂️", url="https://t.me/AgentAvaniG"), InlineKeyboardButton("ᴄᴏʟʟᴀʙᴏʀᴀᴛɪᴏɴ 💬", url="https://t.me/RgC21")]
        ])
        await client.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=welcome_message,
            reply_markup=reply_markup
        )
        #await message.reply_text(welcome_message, reply_markup=reply_markup)
    else:
        join_channels_message = (
            "**😎To use the BOT 🤖  you must join the below channels otherwise you can't access the bot**\n\n"
            "**🤝JOIN & GET BENIFITS👇**"
        )
        reply_markup = generate_join_channels_keyboard()
        await message.reply_text(join_channels_message, reply_markup=reply_markup)

async def on_callback_query(client, callback_query):
    chat_id = callback_query.message.chat.id
    data = callback_query.data
    if data == "check_joined":
        if await check_user_joined_channels(client, callback_query.from_user.id, config.REQUIRED_CHANNEL_IDS):
            await callback_query.message.edit(
                "Thank you for joining the channels! How can I assist you today?",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Get Started", callback_data="get_started")]
                    ]
                )
            )
        else:
            await callback_query.answer("Please join all required channels first.", show_alert=True)

    elif data == "get_started":
        welcome_message = (
            "**👀 𝗧𝗲𝗹𝗹 𝗺𝗲 𝗛𝗼𝘄 𝗰𝗮𝗻 𝗜 𝗵𝗲𝗹𝗽 𝘆𝗼𝘂?**\n"
            "**🤝 मैं आपकी कैसे मदद कर सकती हूँ?**\n\n"
            "**💡ꜰɪʀꜱᴛ ꜱᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴜɪᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ᴀɴᴅ ɪꜰ ʏᴏᴜ ɴᴏᴛ ʀᴇɢɪꜱᴛᴇʀ ᴜɴᴅᴇʀ ᴏꜰꜰɪᴄɪᴀʟ(ᴍʏ) ʟɪɴᴋ ᴏʀ ɪɴ ᴍʏ ᴛᴇᴀᴍ ᴛʜᴇɴ ᴅᴏɴ'ᴛ ᴡᴀꜱᴛᴇ ᴏᴜʀ ᴛɪᴍᴇ.**\n\n"
            "**☞ Rᴇɢɪsᴛᴇʀ Wɪᴛʜ https://bdgwin.com/#/register?invitationCode=48854928**\n\n"
            "**👋 Eᴀʀɴ Dᴀɪʟʏ 2000₹-5000₹ Vɪᴀ Pʟᴀʏɪɴɢ Eᴀsʏ Gᴀᴍᴇs💰**\n\n"
            "**ᴛʜᴀɴᴋ ʏᴏᴜ 😘😘**\n"
            "**────────────────────────────**"
        )
          
        photo_url = "https://telegra.ph/file/a3852757146a2c0fcc184.jpg"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʀᴇᴄʜᴀʀɢᴇ / ᴡɪᴛʜᴅʀᴀᴡᴀʟ ɪꜱꜱᴜᴇ", url="https://t.me/lauraBDG66666")],
            [InlineKeyboardButton("ᴠɪᴘ ᴄʜᴀɴɴᴇʟ", url="https://t.me/+Fp_scQvsGKsyZDhl")],
            [InlineKeyboardButton("ʙᴇᴄᴏᴍᴇ ᴀɢᴇɴᴛ 🤵‍♂️", url="https://t.me/AgentAvaniG"), InlineKeyboardButton("ᴄᴏʟʟᴀʙᴏʀᴀᴛɪᴏɴ 💬", url="https://t.me/RgC21")]
        ])
        await client.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=welcome_message,
            reply_markup=reply_markup
        )

app.add_handler(MessageHandler(start, filters.command("start")))
app.add_handler(CallbackQueryHandler(on_callback_query))

app.run()
        

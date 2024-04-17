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
          f"**Hello {user_full_name}**\n\n"
          "__HOW CAN I HELP YOU ?__\n\n\n"
          "**- BDGWIN SUPPORT**"
        )
          
        photo_url = "https://telegra.ph/file/71e9f02b42bb39d10c1f2.jpg"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("RECHARGE ISSUE", callback_data="TC_LOTTERY_CALLBACK_DATA")],
            [InlineKeyboardButton("AGENT BONUSES", callback_data="OK_WIN_CALLBACK_DATA")],
            [InlineKeyboardButton("GIFT CODE GROUP", callback_data="LIC_GAMES_CALLBACK_DATA")],
            [InlineKeyboardButton("VIP PREDICTIONS", callback_data="RAJALUCK_CALLBACK_DATA")]
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
            "**To use the bot you must first subscribe here ⤵️**"
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

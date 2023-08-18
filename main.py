from pyrogram import Client, filters
from imgurpython import ImgurClient
from datetime import datetime
from config import Cfg
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from messages import Msg
import os

imgur_client = ImgurClient(Cfg.client_id, Cfg.client_secret)
bot = Client("imgur_bot", api_id=Cfg.api_id, api_hash=Cfg.api_hash, bot_token=Cfg.bot_token)

print("Bot is starting...")

# COMMAND HANDLER FOR /START
@bot.on_message(filters.command("start"))
def start(client, message):
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Imgur Website", url="https://imgur.com/"),
            InlineKeyboardButton("Source Code", url="https://github.com/CallMeDimas/Imgur-Telegram_Bot/")
        ]]
    )
    message.reply_text(Msg.onstart, reply_markup=keyboard)

# COMMAND HANDLER FOR /ABOUT
@bot.on_message(filters.command("about"))
def about(client, message):
    message.reply_text(Msg.onabout)

# COMMAND HANDLER FOR /HELP
@bot.on_message(filters.command("help"))
def help(client, message):
    message.reply_text(Msg.onhelp)

# COMMAND HANDLER FOR UPLOADING IMAGE
@bot.on_message(filters.photo)
def upload_image(client, message):
    user = message.from_user
    file_id = message.photo.file_id
    file_path = bot.download_media(file_id)
    filename = f"user_{user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    os.rename(file_path, filename)
    print(f"Received photo from {user.first_name}")
    response = imgur_client.upload_from_path(filename, config=None, anon=True)
    os.remove(filename)
    message.reply_text(f"🎉 Success! Your image has taken flight and landed safely on Imgur: {response['link']}\n\nThank you for choosing our bot for your image sharing needs. We’re thrilled to have been part of your journey today! 🌟\n\nMade with 💙 by @CallMeDimas_bot. Until next time! 👋")

print("Bot is online and ready to use.")
bot.run()

import os
from telethon import TelegramClient

bot = TelegramClient('bot', os.getenv('API_ID'), os.getenv('API_HASH'))
async def run():
	await bot.start(bot_token=os.getenv('TOKEN'))
	await bot.catch_up()
	await bot.run_until_disconnected()
from telethon import events
from telethon.types import Message
import asyncio
import traceback
from datetime import datetime
import random
from math import ceil
import time
import html

from db_config import start as db_start, db
from bot_config import run as run_bot, bot, command_to_regex
from config import *

from last_request import LastRequest
from last_username import LastUsername
from rating import Rating

def none_to_str(s: str | None, default: str='') -> str:
	if s is None:
		return default
	return s

def get_username_raw(user):
	return f'{none_to_str(user.first_name)} {none_to_str(user.last_name)}'

def escape_username(username):
	return html.escape(username).replace('/', '/&NoBreak;')

async def update_sender(msg):
	await LastUsername.update(msg.sender_id, get_username_raw(msg.sender))

@bot.on(events.NewMessage(pattern=command_to_regex('mmr')))
async def mmr(msg: Message):
	await update_sender(msg)

	user_id = msg.sender_id
	group_id = msg.chat.id

	now = datetime.now()
	async with db.transaction():
		last = await LastRequest.get(user_id, group_id)
		if last is not None:
			left = ceil(cooldown - (now - last).total_seconds())
			if left > 0:
				await msg.reply(f'Потрібно зачекати ще {time.strftime("%H:%M:%S", time.gmtime(left))}')
				return
		
		await LastRequest.update(user_id, group_id)
	
	rating = await Rating.get(user_id, group_id)
	delta = 0
	while delta == 0:
		delta = random.randint(max(-rating, mn), mx)
	
	rating += delta
	await Rating.update(user_id, group_id, rating)
	
	await msg.reply(f'Твій рейтинг {"виріс" if delta > 0 else "зменшився"} на {abs(delta)} MMR. Тепер твій рейтинг {rating} MMR.')

async def stringify_top(group_id: int, limit: int=None) -> str:
	top = await Rating.get_top_with_names(group_id, limit)

	info = f'Топ{"" if limit is None else " " + str(limit)} по MMR:\n\n'
	for i, (username, rating) in enumerate(top, 1):
		line = f'{i}) {escape_username(username)} — {rating} MMR\n'
		if len(info) + len(line) > 4096:
			break
		info += line
	print(info)
	return info

@bot.on(events.NewMessage(pattern=command_to_regex('top')))
async def top(msg: Message):
	await update_sender(msg)
	await msg.reply(await stringify_top(msg.chat.id))

@bot.on(events.NewMessage(pattern=command_to_regex('top10')))
async def top10(msg: Message):
	await update_sender(msg)
	await msg.reply(await stringify_top(msg.chat.id, 10))

async def main():
	try:
		await db_start()
		await run_bot()
	except asyncio.CancelledError:
		pass
	except BaseException:
		traceback.print_exc()

asyncio.run(main())
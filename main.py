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
from message_cleanup import run as run_cleanup, queue_message
from config import cooldown, mn, mx

from last_request import LastRequest
from last_username import LastUsername
from rating import Rating

def none_to_str(s: str | None, default: str='') -> str:
	if s is None:
		return default
	return s

def get_username_raw(user):
	return ' '.join([none_to_str(i) for i in (user.first_name, user.last_name)])

def escape_username(username):
	return html.escape(username).replace('/', '/&NoBreak;')

async def update_sender(msg):
	await LastUsername.update(msg.sender_id, get_username_raw(msg.sender))

def command(command: str):
	def inner(func):
		@bot.on(events.NewMessage(pattern=command_to_regex(command)))
		async def handler(msg: Message):
			await update_sender(msg)
			await queue_message(msg)
			return await func(msg)
	return inner

@command('mmr')
async def mmr(msg: Message):
	user_id = msg.sender_id
	group_id = msg.chat_id

	async with db.transaction():
		last = await LastRequest.get(user_id, group_id)
		if last is not None:
			left = ceil((last + cooldown - datetime.now()).total_seconds())
			if left > 0:
				r = await msg.reply(f'Потрібно зачекати ще {time.strftime("%H:%M:%S", time.gmtime(left))}')
				await queue_message(r)
				return
		
		await LastRequest.update(user_id, group_id)
	
	rating = await Rating.get(user_id, group_id)
	delta = 0
	while delta == 0:
		delta = random.randint(max(-rating, mn), mx)
	
	rating += delta
	await Rating.update(user_id, group_id, rating)
	
	r = await msg.reply(f'Твій рейтинг {"виріс" if delta > 0 else "зменшився"} на {abs(delta)} MMR. Тепер твій рейтинг {rating} MMR.')
	await queue_message(r)

async def stringify_top(group_id: int, limit: int=None) -> str:
	top = await Rating.get_top_with_names(group_id, limit)

	info = f'Топ{"" if limit is None else " " + str(limit)} по MMR:\n\n'
	for i, (username, rating) in enumerate(top, 1):
		line = f'{i}) {escape_username(username)} — {rating} MMR\n'
		if len(info) + len(line) > 4096:
			break
		info += line
	return info

@command('top')
async def top(msg: Message):
	await queue_message(await msg.reply(await stringify_top(msg.chat_id)))

@command('top10')
async def top10(msg: Message):
	await queue_message(await msg.reply(await stringify_top(msg.chat_id, 10)))

async def main():
	try:
		await db_start()
		await asyncio.gather(run_cleanup(), run_bot())
	except asyncio.CancelledError:
		pass
	except BaseException:
		traceback.print_exc()

asyncio.run(main())
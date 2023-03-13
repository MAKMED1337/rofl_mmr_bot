from datetime import datetime
from telethon.types import Message
import asyncio

from config import cleanup_timeout
from bot_config import bot
from messages_cleanup_db import MessagesCleanup

async def queue_message(msg: Message):
	await MessagesCleanup.add(msg.chat_id, msg.id, msg.date)
	asyncio.create_task(cleanup_after_timeout())
	
async def cleanup():
	while True:
		msg = await MessagesCleanup.get_first()
		if msg is None:
			break
		
		if (datetime.utcnow() - msg.date).total_seconds() < cleanup_timeout:
			break

		try:
			await bot.delete_messages(msg.group_id, msg.message_id)
		except BaseException:
			pass
		finally:
			await MessagesCleanup.remove(msg.group_id, msg.message_id)

async def cleanup_after_timeout():
	await asyncio.sleep(cleanup_timeout)
	await cleanup()

async def run():
	while True:
		await cleanup_after_timeout()
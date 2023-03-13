from db_config import Base, db
from sqlalchemy import Column, BIGINT, DateTime
from sqlalchemy import select, insert, delete, and_

from datetime import datetime
from typing import Union

class MessagesCleanup(Base):
	__tablename__ = 'messages_cleanup'
	group_id = Column(BIGINT, primary_key=True)
	message_id = Column(BIGINT, primary_key=True)
	date = Column(DateTime)

	@staticmethod
	async def add(group_id: int, message_id: int, sent_date: datetime):
		await db.execute(insert(MessagesCleanup).values((group_id, message_id, sent_date)))

	@staticmethod
	async def get_first() -> Union['MessagesCleanup', None]:
		return await db.fetch_one(select(MessagesCleanup).order_by(MessagesCleanup.date))

	@staticmethod
	async def remove(group_id: int, message_id: int):
		await db.execute(delete(MessagesCleanup).where(and_(MessagesCleanup.group_id == group_id, MessagesCleanup.message_id == message_id)))
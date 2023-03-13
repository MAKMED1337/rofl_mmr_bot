from db_config import Base, db, fetch_one_column
from sqlalchemy import Column, BIGINT, DateTime
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import select, update, and_
from sqlalchemy.sql import func

class LastRequest(Base):
	__tablename__ = 'last_request'
	user_id = Column(BIGINT, primary_key=True)
	group_id = Column(BIGINT, primary_key=True)
	last_request = Column(DateTime)

	@staticmethod
	async def get(user_id: int, group_id: int) -> DateTime | None:
		return await fetch_one_column(select(LastRequest.last_request).where(and_(LastRequest.user_id == user_id, LastRequest.group_id == group_id)))

	@staticmethod
	async def update(user_id: int, group_id: int):
		await db.execute(insert(LastRequest).values((user_id, group_id, func.now())).on_duplicate_key_update(last_request=func.now()))
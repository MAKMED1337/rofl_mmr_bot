from db_config import Base, db, fetch_one_column
from sqlalchemy import Column, BIGINT, TEXT
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import select, and_

class LastUsername(Base):
	__tablename__ = 'last_username'
	user_id = Column(BIGINT, primary_key=True)
	username = Column(TEXT, nullable=False)

	@staticmethod
	async def update(user_id: int, username: int):
		await db.execute(insert(LastUsername).values((user_id, username)).on_duplicate_key_update(username=username))

	@staticmethod
	async def get_username(user_id: int) -> str:
		return await fetch_one_column(select(LastUsername.username).where(LastUsername.user_id == user_id))
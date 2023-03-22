from .config import Base, db
from sqlalchemy import Column, BIGINT, TEXT
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import select

class LastUsername(Base):
	__tablename__ = 'last_username'
	user_id = Column(BIGINT, primary_key=True)
	username = Column(TEXT, nullable=False)

	@staticmethod
	async def update(user_id: int, username: int):
		await db.execute(insert(LastUsername).values((user_id, username)).on_duplicate_key_update(username=username))

	@staticmethod
	async def get_username(user_id: int) -> str:
		return await db.fetch_val(select(LastUsername.username).where(LastUsername.user_id == user_id))
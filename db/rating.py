from .config import Base, db
from sqlalchemy import Column, BIGINT, DateTime
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import select, and_
from .last_username import LastUsername

class Rating(Base):
	__tablename__ = 'rating'
	user_id = Column(BIGINT, primary_key=True)
	group_id = Column(BIGINT, primary_key=True)
	rating = Column(BIGINT, nullable=False, default=0, server_default='0')

	@staticmethod
	async def get(user_id: int, group_id: int) -> DateTime | None:
		r = await db.fetch_val(select(Rating.rating).where(and_(Rating.user_id == user_id, Rating.group_id == group_id)))
		return 0 if r is None else r

	@staticmethod
	async def update(user_id: int, group_id: int, rating: int):
		await db.execute(insert(Rating).values((user_id, group_id, rating)).on_duplicate_key_update(rating=rating))

	@staticmethod
	async def get_top(group_id: int, limit: int=None) -> list['Rating']:
		return await db.fetch_all(select(Rating).where(Rating.group_id == group_id).order_by(Rating.rating.desc()).limit(limit))

	@staticmethod
	async def get_top_with_names(group_id: int, limit: int=None) -> list[tuple[str, int]]:
		stmt = select(LastUsername.username, Rating.rating).join(Rating, Rating.user_id == LastUsername.user_id).where(Rating.group_id == group_id).order_by(Rating.rating.desc()).limit(limit)
		return await db.fetch_all(stmt)
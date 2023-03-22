import os
from sqlalchemy.orm import declarative_base
import sqlalchemy
import databases
from urllib.parse import quote_plus
from sqlalchemy.sql import ClauseElement
from databases.interfaces import Record

Base = declarative_base()
DATABASE_ARGS = f'://root_db:{quote_plus(os.getenv("db_pass"))}@localhost/mmr_bot'
engine = sqlalchemy.create_engine('mysql' + DATABASE_ARGS)
db = databases.Database('mysql+asyncmy' + DATABASE_ARGS + '?pool_recycle=3600')

async def fetch_all_column(query: ClauseElement | str, values: dict = None) -> list[Record]:
	return [r[0] for r in await db.fetch_all(query, values)]

async def start():
	Base.metadata.create_all(engine)
	await db.connect()
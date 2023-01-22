import typing as tp

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy.sql import select


metadata = MetaData()


def init_db(config: dict[str, tp.Any]):
    config_db = config['database']
    engine = create_async_engine(config_db['DB_URL'], echo=config_db['DB_ECHO'])
    return engine


async def get_assignments_for_user(conn: AsyncConnection, id: int):
    users = metadata.tables['users']
    assignments = metadata.tables['assignments']

    j = assignments.join(users, assignments.c.user_id == users.c.user_id)
    stmt = (
        select(assignments)
        .select_from(j)
        .where(users.c.user_id == id)
        .order_by(assignments.c.parking_day)
    )
    records = await conn.execute(stmt)
    return records

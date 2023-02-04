import typing as tp

from datetime import datetime as dt

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy.sql import select, insert, and_, func

import sqlite3

metadata = MetaData()


def use_inspector(conn):
    """Workaround as SQLAlchemy does not yet offer asyncio version of Inspector.

    https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-the-inspector-to-inspect-schema-objects
    """
    metadata.reflect(bind=conn)


def init_db(config: dict[str, tp.Any]):
    config_db = config['database']
    engine = create_async_engine(
        config_db['DB_URL'],
        echo=config_db['DB_ECHO'],
        connect_args={'detect_types': sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES},
        native_datetime=True,
    )
    return engine


async def get_requestors_ids(conn: AsyncConnection, date: dt.date) -> list[int]:
    users = metadata.tables['users']
    statuses = metadata.tables['statuses']
    workflow = metadata.tables['workflow']

    j = workflow.join(users, workflow.c.user_id == users.c.user_id).join(
        statuses, workflow.c.status_id == statuses.c.status_id
    )
    stmt = (
        select(users.c.user_id, func.max(workflow.c.timestamp))
        .select_from(j)
        .where(
            and_(
                workflow.c.status_id.in_([100, 210, 301, 310]),
                workflow.c.parking_day == date,
            )
        )
        .group_by(workflow.c.user_id)
        .having(statuses.c.status_id.in_([100]))
    )
    records = await conn.execute(stmt)
    return [r[0] for r in records]


async def get_top_users_ids(conn: AsyncConnection) -> list[int, int]:
    users = metadata.tables['users']
    statuses = metadata.tables['statuses']
    workflow = metadata.tables['workflow']

    j = workflow.join(users, workflow.c.user_id == users.c.user_id).join(
        statuses, workflow.c.status_id == statuses.c.status_id
    )
    stmt = (
        select(workflow.c.user_id, func.count(workflow.c.user_id))
        .select_from(j)
        .where(workflow.c.status_id.in_([401, 402]))
        .group_by(workflow.c.user_id)
        .order_by(workflow.c.user_id)
    )
    records = await conn.execute(stmt)
    return list(records)


async def save_lottery_results(
    conn: AsyncConnection, parking_day: dt, winners: list[int], losers: list[int]
) -> None:
    workflow = metadata.tables['workflow']

    await conn.execute(
        insert(workflow),
        [
            {
                'timestamp': dt.now(),
                'parking_day': parking_day,
                'status_id': 301,
                'user_id': id,
            }
            for id in winners
        ],
    )

    await conn.execute(
        insert(workflow),
        [
            {
                'timestamp': dt.now(),
                'parking_day': parking_day,
                'status_id': 310,
                'user_id': id,
            }
            for id in losers
        ],
    )

    await conn.commit()

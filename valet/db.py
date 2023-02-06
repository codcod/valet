"""
Database connection and operations.
"""

import sqlite3
from datetime import datetime as dt

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine
from sqlalchemy.sql import and_, func, insert, select, text

from . import const
from .types_ import ValetConfig, Winnings

metadata = MetaData()


def use_inspector(conn):
    """Workaround as SQLAlchemy does not yet offer asyncio version of Inspector.

    https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-the-inspector-to-inspect-schema-objects
    """
    metadata.reflect(bind=conn)


def init_db(config: ValetConfig):
    """
    Initialize database based on configuration.

    Passes additional arguments to the underlying `sqlite3` driver.
    """
    config_db = config['database']
    engine = create_async_engine(
        config_db['DB_URL'],
        echo=config_db['DB_ECHO'],
        connect_args={'detect_types': sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES},
        native_datetime=True,
    )
    return engine


async def select_requestors(conn: AsyncConnection, parking_day: dt.date) -> list[int]:
    """
    Select all users requesting a parking spot on a given day and return their ids.
    """
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
                workflow.c.status_id.in_(
                    [
                        const.STATUS_REQUESTED,
                        const.STATUS_CANCELLED,
                        const.STATUS_WON,
                        const.STATUS_LOST,
                    ]
                ),
                workflow.c.parking_day == parking_day,
            )
        )
        .group_by(workflow.c.user_id)
        .having(statuses.c.status_id.in_([const.STATUS_REQUESTED]))
    )
    records = await conn.execute(stmt)
    return [r[0] for r in records]


async def past_winnings(conn: AsyncConnection) -> Winnings:
    """
    Select users who until now won the lottery for a parking spot at least one
    time and how many times they won.

    The count of wins is used as a weight for a lottery draw.
    """
    users = metadata.tables['users']
    statuses = metadata.tables['statuses']
    workflow = metadata.tables['workflow']

    j = workflow.join(users, workflow.c.user_id == users.c.user_id).join(
        statuses, workflow.c.status_id == statuses.c.status_id
    )
    stmt = (
        select(workflow.c.user_id, func.count(workflow.c.user_id))
        .select_from(j)
        .where(workflow.c.status_id.in_([const.STATUS_USED, const.STATUS_UNCONFIRMED]))
        .group_by(workflow.c.user_id)
        .order_by(workflow.c.user_id)
    )
    records = await conn.execute(stmt)
    return dict(list(records))


async def available_parking_spots(
    conn: AsyncConnection, parking_day: dt.date
) -> list[int]:
    """
    Select parking spots that are available on a given day and return their ids.
    """
    stmt = text(
        '''
    select spot_id from spots
    where spot_id in (
        select spot_id as id from spots
        except
        select assignment_id as id from assignments
        where parking_day = :day
    )'''
    )
    records = await conn.execute(stmt, {'day': parking_day})
    return [r[0] for r in records]


async def save_results(
    conn: AsyncConnection,
    parking_day: dt,
    winners: list[int],
    parking_spots: list[int],
    losers: list[int] = None,
) -> None:
    """
    Save lottery results.
    """
    workflow = metadata.tables['workflow']
    assignments = metadata.tables['assignments']

    # store winners
    await conn.execute(
        insert(workflow),
        [
            {
                'timestamp': dt.now(),
                'parking_day': parking_day,
                'status_id': const.STATUS_WON,
                'user_id': id,
            }
            for id in winners
        ],
    )

    # store parking spots assignments
    await conn.execute(
        insert(assignments),
        [
            {
                'parking_day': parking_day,
                'user_id': user_id,
                'spot_id': spot_id,
            }
            for user_id, spot_id in zip(winners, parking_spots)
        ],
    )

    # store losers
    if losers:
        await conn.execute(
            insert(workflow),
            [
                {
                    'timestamp': dt.now(),
                    'parking_day': parking_day,
                    'status_id': const.STATUS_LOST,
                    'user_id': id,
                }
                for id in losers
            ],
        )

    await conn.commit()

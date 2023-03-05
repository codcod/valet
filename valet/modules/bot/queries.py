from datetime import datetime as dt

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql import and_, func, insert, select, text, update

from valet import const
from valet.database import metadata


async def user_standing_requests(conn: AsyncConnection, user_id: int):
    """
    Select all `open` requests of a given user.
    """
    stmt = text(
        '''
    select w.parking_day, s.name as status, max(w.timestamp) as timestamp
    from workflow w
    join users u on u.user_id = w.user_id
    join statuses s on s.status_id = w.status_id
    where 
        u.user_id = :user_id
    group by w.parking_day
    having s.status_id in (100)
    '''
    )
    records = await conn.execute(stmt, {'user_id': user_id})
    return list(records)


async def find_by_slack_id(conn: AsyncConnection, slack_id: str) -> int:
    users = metadata.tables['users']

    stmt = select(users.c.user_id).where(users.c.slack_id == slack_id)
    result = await conn.execute(stmt)
    row = result.first()

    return row.user_id


async def insert_request(conn: AsyncConnection, user_id: int, parking_day: dt.date):
    workflow = metadata.tables['workflow']

    await conn.execute(
        insert(workflow),
        [
            {
                'timestamp': dt.now(),
                'parking_day': parking_day,
                'status_id': const.STATUS_REQUESTED,
                'user_id': user_id,
            }
        ],
    )

    await conn.commit()


async def cancel_request(conn: AsyncConnection, user_id: int, parking_day: dt.date):
    workflow = metadata.tables['workflow']

    await conn.execute(
        update(workflow)
        .where(
            and_(
                workflow.c.user_id == user_id,
                workflow.c.parking_day == parking_day,
                workflow.c.status_id == const.STATUS_REQUESTED,
            )
        )
        .values(status_id=const.STATUS_CANCELLED)
    )

    await conn.commit()

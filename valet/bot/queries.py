from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql import and_, func, insert, select, text


async def user_standing_requests(conn: AsyncConnection, id: int):
    """
    Select parking spots that are available on a given day and return their ids.
    """
    stmt = text(
        '''
    select w.parking_day, s.name, max(w.timestamp)
    from workflow w
    join users u on u.user_id = w.user_id
    join statuses s on s.status_id = w.status_id
    where 
        u.user_id = :id
    group by w.parking_day
    having s.status_id in (100)
    '''
    )
    records = await conn.execute(stmt, {'id': id})
    return list(records)

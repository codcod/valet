from datetime import datetime as dt

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql import and_, func, insert, select, text

from valet import const
from valet.database import metadata
from valet.types import Winnings


async def requestors_for_given_day(
    conn: AsyncConnection, parking_day: dt.date
) -> list[int]:
    """
    Select all users requesting a parking spot on a given day and return their ids.

    See also: `valet.modules.web.queries.requestors_for_given_day()`
    """
    users = metadata.tables['users']
    statuses = metadata.tables['statuses']
    workflow = metadata.tables['workflow']

    j = workflow.join(users, workflow.c.user_id == users.c.user_id).join(
        statuses, workflow.c.status_id == statuses.c.status_id
    )
    stmt = (
        select(workflow.c.user_id, func.max(workflow.c.timestamp))
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
        .group_by(workflow.c.user_id, statuses.c.status_id)
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


async def save_lottery_results(
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


async def user_standing_requests(conn: AsyncConnection, user_id: int):
    """
    Select all `open` requests of a given user.
    """
    stmt = text(
        '''
    select w.parking_day, s.name, max(w.timestamp)
    from workflow w
    join users u on u.user_id = w.user_id
    join statuses s on s.status_id = w.status_id
    where 
        u.user_id = :user_id
    group by w.parking_day
    having s.status_id in (100)
    '''
    )
    records = await conn.execute(stmt, {'id': user_id})
    return list(records)

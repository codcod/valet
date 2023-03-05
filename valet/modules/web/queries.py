from datetime import datetime as dt

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql import and_, func, insert, select, text

from valet import const
from valet.database import metadata


async def requestors_for_given_day(
    conn: AsyncConnection, parking_day: dt.date
) -> list[int]:
    """
    Select all users requesting a parking spot on a given day and return their ids.

    See also: `valet.modules.job.queries.requestors_for_given_day()`
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

"""Recurring job to run lottery on selected days in the future.

Before the lottery users who requested a parking spot on a given day are
selected. Out of them winners are drawn based on how many parking spots there
are. Afterwards the winners and the users who did not get a spot are stored in
the database.

Intended to be a main module (hence absolute imports).
"""

import typing as tp
from datetime import datetime as dt

from sqlalchemy.ext.asyncio import AsyncConnection

from valet import database, date
from valet.job import lottery
from valet.job import queries as db
from valet.logging import get_logger

logger = get_logger(__name__)


async def run_lottery(conn: AsyncConnection, parking_day: dt.date) -> None:
    """
    Run the lottery for a given parking day and subsequently assign parking spots.
    """
    requestors = await db.requestors_for_given_day(conn, parking_day)
    if requestors:
        logger.debug(f'{requestors=}')
    else:
        logger.debug(f'No requests for parking day={parking_day:%Y-%m-%d, %A}')
        return

    parking_spots = await db.available_parking_spots(conn, parking_day)
    k = len(parking_spots)
    logger.debug(f'{k=} | {parking_spots=}')

    if k <= 0:
        logger.debug('For some reason there are no parking spots left')
        return

    if len(requestors) <= k:
        await db.save_lottery_results(conn, parking_day, requestors, parking_spots)

    elif len(requestors) > k:
        past_winnings = await db.past_winnings(conn)
        logger.debug(f'{past_winnings=}')

        winners = lottery.draw(requestors, past_winnings, k)
        logger.debug(f'{winners=}')

        if winners:
            losers = [user for user in requestors if user not in winners]
            await db.save_lottery_results(
                conn, parking_day, winners, parking_spots, losers
            )
        else:
            logger.debug('There are no winners, nothing to save')


async def run_job():
    """
    Main part of the job.
    """
    engine = await database.get_engine()

    async with engine.connect() as conn:
        d = dt(2022, 12, 28).date()  # FIXME: for testing
        for day in date.range(start=d):
            logger.debug(f'Running the lottery for parking {day=:%Y-%m-%d, %A}')
            await run_lottery(conn, day)

    await engine.dispose()

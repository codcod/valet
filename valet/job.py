"""Recurring job to run lottery on selected days in the future.

Before the lottery users who requested a parking spot on a given day are
selected. Out of them winners are drawn based on how many parking spots there
are. Afterwards the winners and the users who did not get a spot are stored in
the database.

Intended to be a main module (hence absolute imports).
"""

import asyncio
import logging
import time
import typing as tp
from datetime import datetime as dt
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from valet import db, lottery, settings
from valet.types_ import ValetConfig

logger = logging.getLogger(__name__)


def setup_logging(config: ValetConfig) -> None:
    """
    Setup logging for the job.
    """
    level = logging.getLevelName(logging.DEBUG)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(module)s] %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S %Z",
    )
    logging.Formatter.converter = time.localtime


async def setup_db(config: ValetConfig) -> None:
    """
    Set up the database connection.
    """
    engine = db.init_db(config)

    async with engine.connect() as conn:
        await conn.run_sync(db.use_inspector)

    return engine


async def teardown_db(engine: AsyncEngine) -> None:
    """
    Dispose the access to the database.
    """
    await engine.dispose()


def date_range(
    start: dt.date = dt.today().date(), days: int = 5
) -> tp.Generator[dt.date, None, None]:
    """
    Generates 'days' days starting with the next Monday after the `start` day.
    """
    until_monday = 7 - start.isoweekday() + 1
    monday = start + timedelta(days=until_monday)
    return (monday + timedelta(days=d) for d in range(days))


async def run_lottery(conn: AsyncConnection, parking_day: dt.date):
    """
    Run the lottery for a given parking day.
    """
    requestors = await db.select_requestors(conn, parking_day)
    if requestors:
        logger.debug(f'{requestors=}')
    else:
        logger.debug(f'No requests for parking day={parking_day:%Y-%m-%d, %A}')
        return

    past_winnings = await db.past_winnings(conn)
    logger.debug(f'{past_winnings=}')

    parking_spots = await db.available_parking_spots(conn, parking_day)
    k = len(parking_spots)
    logger.debug(f'{k=}')

    winners = lottery.draw(requestors, past_winnings, k)
    logger.debug(f'{winners=}')

    if winners:
        losers = [user for user in requestors if user not in winners]
        await db.save_results(conn, parking_day, winners, parking_spots, losers)
    else:
        logger.debug('There are no winners, nothing to save')


async def main():
    """
    Main part of the job.
    """
    config = settings.load_config('config/config.toml')
    setup_logging(config)

    engine: AsyncEngine = await setup_db(config)

    async with engine.connect() as conn:
        d = dt(2022, 12, 28).date()  # FIXME: for testing
        for day in date_range(start=d):
            logger.debug(f'Running the lottery for parking {day=:%Y-%m-%d, %A}')
            await run_lottery(conn, day)

        await teardown_db(engine)


if __name__ == '__main__':
    asyncio.run(main())

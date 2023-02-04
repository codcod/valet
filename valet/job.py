"""Recurring job to run lottery on selected days in the future.

Before the lottery users who requested a parking spot on a given day are
selected. Out of them winners are drawn based on how many parking spots there
are. Afterwards the winners and the users who did not get a spot are stored in
the database.
"""

import asyncio
import logging
import time
from datetime import datetime as dt

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection

from valet import db
from valet.settings import load_config
from valet.lottery import draw


logger = logging.getLogger(__name__)


def setup_lopgging() -> None:
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


async def setup() -> None:
    """
    Set up the database connection.
    """
    config = load_config('config/config.toml')
    engine = db.init_db(config)

    async with engine.connect() as conn:
        await conn.run_sync(db.use_inspector)

    return engine


async def teardown(engine: AsyncEngine) -> None:
    """
    Dispose the access to the database.
    """
    await engine.dispose()


def choose_days_for_lottery() -> list[dt.date]:
    """
    Choose future days to target the lottery for.
    """
    day = dt.strptime('2023-01-02', '%Y-%m-%d').date()
    return [day]


async def run_lottery(conn: AsyncConnection, parking_day: dt.date):
    """
    Run the lottery for a given parking day.
    """
    players = await db.get_requestors_ids(conn, parking_day)
    if players:
        logger.debug(f'{players=}')
    else:
        logger.debug(f'No requestors for parking day={parking_day:%Y-%m-%d, %A}')
        return

    top_users = await db.get_top_users_ids(conn)
    logger.debug(f'{top_users=}')

    winners = draw(players, top_users)
    logger.debug(f'{winners=}')

    if winners:
        await db.save_lottery_results(
            conn,
            parking_day,
            winners,
            [user for user in players if user not in winners],
        )
    else:
        logger.debug('There are no winners, nothing to save')


async def main():
    """
    Main part of the job.
    """
    setup_lopgging()

    engine: AsyncEngine = await setup()

    async with engine.connect() as conn:
        days = choose_days_for_lottery()
        for day in days:
            logger.debug(f'Running the lottery for parking {day=:%Y-%m-%d, %A}')
            await run_lottery(conn, day)

        await teardown(engine)


if __name__ == '__main__':
    asyncio.run(main())

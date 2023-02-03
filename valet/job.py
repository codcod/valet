"""Recurring job to choose winners out of requestors."""

import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncEngine

from valet import db
from valet.settings import load_config
from valet.lottery import draw


async def setup() -> None:
    config = load_config('config/config.toml')
    engine = db.init_db(config)

    async with engine.connect() as conn:
        await conn.run_sync(db.use_inspector)

    return engine


async def teardown(engine: AsyncEngine) -> None:
    await engine.dispose()


async def main():
    engine: AsyncEngine = await setup()

    async with engine.connect() as conn:
        players = await db.get_requestors_ids(conn, '2023-01-02')
        print(f'{players=}')

        top_users = await db.get_top_users_ids(conn)
        print(f'{top_users=}')

        winner_id = draw(players, top_users)
        print(f'{winner_id=}')

        # insert into workflow (timestamp, parking_day, user_id, status_id)
        # values (now(), "2023-01-01", $winner_id, 301)

        # insert into workflow (timestamp, parking_day, user_id, status_id)
        # values (now(), "2023-01-01", $players-winner_id, 310)

        await teardown(engine)


if __name__ == '__main__':
    asyncio.run(main())

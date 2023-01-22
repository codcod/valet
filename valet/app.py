import logging

from aiohttp import web

from valet import db
from valet.views import routes
from valet.settings import load_config


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def use_inspector(conn):
    """Workaround as SQLAlchemy does not yet offer asyncio version of Inspector.

    https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-the-inspector-to-inspect-schema-objects
    """
    db.metadata.reflect(bind=conn)


async def setup_app(app: web.Application) -> None:
    config = load_config('config/config.toml')
    engine = db.init_db(config)

    app['config'] = config
    app['engine'] = engine

    async with engine.connect() as conn:
        await conn.run_sync(use_inspector)


async def teardown_app(app: web.Application) -> None:
    engine = app['engine']
    await engine.dispose()


async def make_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(setup_app)
    app.on_cleanup.append(teardown_app)
    app.add_routes(routes)
    return app
